// --- Affordability calculator ---------------------------------------
(() => {
  const panel = document.querySelector('[data-calculator]');
  if (!panel) return;

  const priceRange = panel.querySelector('[data-calc-price-range]');
  const priceInput = panel.querySelector('[data-calc-price]');
  const priceReadout = panel.querySelector('[data-calc-price-readout]');
  const depositInput = panel.querySelector('[data-calc-deposit]');
  const depositReadout = panel.querySelector('[data-calc-deposit-readout]');
  const rateInput = panel.querySelector('[data-calc-rate]');
  const rateToggle = panel.querySelector('[data-calc-rate-toggle]');
  const termInput = panel.querySelector('[data-calc-term]');
  const termReadout = panel.querySelector('[data-calc-term-readout]');
  const costsInput = panel.querySelector('[data-calc-costs]');

  const depositAmountOut = panel.querySelector('[data-calc-deposit-amount]');
  const loanOut = panel.querySelector('[data-calc-loan]');
  const financedPctOut = panel.querySelector('[data-calc-financed-pct]');
  const totalInterestOut = panel.querySelector('[data-calc-total-interest]');
  const costsAmountOut = panel.querySelector('[data-calc-costs-amount]');
  const totalPropertyOut = panel.querySelector('[data-calc-total-property]');
  const cashWithMortgageOut = panel.querySelector('[data-calc-cash-with-mortgage]');
  const monthlyOut = panel.querySelector('[data-calc-monthly]');

  const barDeposit = panel.querySelector('[data-calc-bar-deposit]');
  const barPrincipal = panel.querySelector('[data-calc-bar-principal]');
  const barInterest = panel.querySelector('[data-calc-bar-interest]');

  const formatEuro = (value) => `€${Math.round(Math.max(0, value)).toLocaleString('en-US')}`;

  rateToggle?.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-rate-type]');
    if (!button) return;
    rateToggle.querySelectorAll('button').forEach((btn) => btn.classList.toggle('is-active', btn === button));
    update();
  });

  function update() {
    const price = Math.max(0, Number(priceInput.value) || 0);
    const depositPct = Number(depositInput.value) || 0;
    const rate = Number(rateInput.value) || 0;
    const years = Number(termInput.value) || 0;
    const costsPct = Number(costsInput.value) || 0;

    const depositAmount = price * (depositPct / 100);
    const loanAmount = Math.max(0, price - depositAmount);
    const months = Math.max(1, Math.round(years * 12));
    const monthlyRate = rate / 100 / 12;

    let monthlyPayment;
    if (monthlyRate === 0) {
      monthlyPayment = loanAmount / months;
    } else {
      const factor = Math.pow(1 + monthlyRate, months);
      monthlyPayment = loanAmount * (monthlyRate * factor) / (factor - 1);
    }

    const totalRepaid = monthlyPayment * months;
    const totalInterest = Math.max(0, totalRepaid - loanAmount);
    const costsAmount = price * (costsPct / 100);
    const totalProperty = price + costsAmount;
    const cashWithMortgage = depositAmount + costsAmount;
    const financedPct = price > 0 ? Math.round((loanAmount / price) * 100) : 0;

    if (priceRange) priceRange.value = String(price);
    priceReadout.textContent = formatEuro(price);
    depositReadout.textContent = `${depositPct}% · ${formatEuro(depositAmount)}`;
    termReadout.textContent = `${years} years`;
    depositAmountOut.textContent = formatEuro(depositAmount);
    loanOut.textContent = formatEuro(loanAmount);
    financedPctOut.textContent = `${financedPct}%`;
    totalInterestOut.textContent = formatEuro(totalInterest);
    costsAmountOut.textContent = formatEuro(costsAmount);
    totalPropertyOut.textContent = formatEuro(totalProperty);
    if (cashWithMortgageOut) cashWithMortgageOut.textContent = formatEuro(cashWithMortgage);
    monthlyOut.textContent = formatEuro(monthlyPayment);

    const barTotal = Math.max(1, depositAmount + loanAmount + totalInterest);
    barDeposit.style.width = `${(depositAmount / barTotal) * 100}%`;
    barPrincipal.style.width = `${(loanAmount / barTotal) * 100}%`;
    barInterest.style.width = `${(totalInterest / barTotal) * 100}%`;
  }

  priceRange?.addEventListener('input', () => {
    priceInput.value = priceRange.value;
    update();
  });

  [priceInput, depositInput, rateInput, termInput, costsInput].forEach((input) => {
    input?.addEventListener('input', update);
  });

  update();
})();
