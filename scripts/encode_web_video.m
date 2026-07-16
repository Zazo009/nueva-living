#import <AVFoundation/AVFoundation.h>
#import <CoreVideo/CoreVideo.h>
#import <Foundation/Foundation.h>

int main(int argc, const char *argv[]) {
  @autoreleasepool {
    if (argc < 4) {
      fprintf(stderr, "Usage: encode_web_video input output bitrate\n");
      return 2;
    }

    NSString *inputPath = [NSString stringWithUTF8String:argv[1]];
    NSString *outputPath = [NSString stringWithUTF8String:argv[2]];
    NSInteger bitrate = [[NSString stringWithUTF8String:argv[3]] integerValue];
    NSURL *inputURL = [NSURL fileURLWithPath:inputPath];
    NSURL *outputURL = [NSURL fileURLWithPath:outputPath];
    AVURLAsset *asset = [AVURLAsset URLAssetWithURL:inputURL options:nil];
    AVAssetTrack *track = [[asset tracksWithMediaType:AVMediaTypeVideo] firstObject];

    if (!track) {
      fprintf(stderr, "Unable to load source video\n");
      return 3;
    }

    NSError *error = nil;
    AVAssetReader *reader = [[AVAssetReader alloc] initWithAsset:asset error:&error];
    if (!reader) {
      fprintf(stderr, "Unable to create video reader: %s\n", error.localizedDescription.UTF8String);
      return 4;
    }

    NSDictionary *readerSettings = @{
      (id)kCVPixelBufferPixelFormatTypeKey: @(kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange)
    };
    AVAssetReaderTrackOutput *readerOutput =
      [[AVAssetReaderTrackOutput alloc] initWithTrack:track outputSettings:readerSettings];
    readerOutput.alwaysCopiesSampleData = NO;
    if (![reader canAddOutput:readerOutput]) {
      fprintf(stderr, "Unable to configure video reader\n");
      return 5;
    }
    [reader addOutput:readerOutput];

    [[NSFileManager defaultManager] removeItemAtURL:outputURL error:nil];
    AVAssetWriter *writer = [[AVAssetWriter alloc] initWithURL:outputURL
                                                     fileType:AVFileTypeMPEG4
                                                        error:&error];
    if (!writer) {
      fprintf(stderr, "Unable to create video writer: %s\n", error.localizedDescription.UTF8String);
      return 6;
    }
    writer.shouldOptimizeForNetworkUse = YES;

    CGSize naturalSize = track.naturalSize;
    NSInteger width = (NSInteger)fabs(naturalSize.width);
    NSInteger height = (NSInteger)fabs(naturalSize.height);
    NSInteger frameRate = MAX(24, (NSInteger)lround(track.nominalFrameRate));
    NSDictionary *compressionSettings = @{
      AVVideoAverageBitRateKey: @(bitrate),
      AVVideoExpectedSourceFrameRateKey: @(frameRate),
      AVVideoMaxKeyFrameIntervalKey: @(frameRate * 2),
      AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
      AVVideoAllowFrameReorderingKey: @NO
    };
    NSDictionary *writerSettings = @{
      AVVideoCodecKey: AVVideoCodecTypeH264,
      AVVideoWidthKey: @(width),
      AVVideoHeightKey: @(height),
      AVVideoCompressionPropertiesKey: compressionSettings
    };
    AVAssetWriterInput *writerInput =
      [[AVAssetWriterInput alloc] initWithMediaType:AVMediaTypeVideo outputSettings:writerSettings];
    writerInput.expectsMediaDataInRealTime = NO;
    writerInput.transform = track.preferredTransform;
    if (![writer canAddInput:writerInput]) {
      fprintf(stderr, "Unable to configure video writer\n");
      return 7;
    }
    [writer addInput:writerInput];

    BOOL writerStarted = [writer startWriting];
    BOOL readerStarted = [reader startReading];
    if (!writerStarted || !readerStarted) {
      fprintf(stderr,
              "Unable to start video encoding (writer: %s, reader: %s, writer error: %s, reader error: %s)\n",
              writerStarted ? "yes" : "no",
              readerStarted ? "yes" : "no",
              writer.error.localizedDescription.UTF8String ?: "none",
              reader.error.localizedDescription.UTF8String ?: "none");
      return 8;
    }
    [writer startSessionAtSourceTime:kCMTimeZero];

    dispatch_semaphore_t completion = dispatch_semaphore_create(0);
    dispatch_queue_t queue = dispatch_queue_create("com.nuevaliving.video-encode", DISPATCH_QUEUE_SERIAL);
    [writerInput requestMediaDataWhenReadyOnQueue:queue usingBlock:^{
      while (writerInput.readyForMoreMediaData) {
        CMSampleBufferRef sample = [readerOutput copyNextSampleBuffer];
        if (!sample) {
          [writerInput markAsFinished];
          [writer finishWritingWithCompletionHandler:^{
            dispatch_semaphore_signal(completion);
          }];
          return;
        }
        BOOL appended = [writerInput appendSampleBuffer:sample];
        CFRelease(sample);
        if (!appended) {
          [reader cancelReading];
          [writerInput markAsFinished];
          [writer cancelWriting];
          dispatch_semaphore_signal(completion);
          return;
        }
      }
    }];

    dispatch_semaphore_wait(completion, DISPATCH_TIME_FOREVER);
    if (writer.status != AVAssetWriterStatusCompleted) {
      fprintf(stderr, "Encoding failed: %s\n", writer.error.localizedDescription.UTF8String);
      return 9;
    }

    printf("Encoded %ldx%ld H.264 at %ld bps\n", (long)width, (long)height, (long)bitrate);
  }
  return 0;
}
