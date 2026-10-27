// Whether a project's real name may be published.
//
// Projects are published under a name of our own and crm.realName holds the
// developer's. A name becomes publishable in one of two ways: the project is
// already published under it (La Morelia, Armani Residences Marbella: the name
// on the page is the name on the sign), or `crm.namePublic` is true, which is
// the decision to publish a project under its own name. The flag lives in the
// crm block on purpose -- that block never reaches a page or the public
// catalogue -- and covers the project's name only. The developer
// (crm.realDeveloper) stays held back, and so does every image check for it.
export function realNameIsPublic(project) {
  const real = String(project?.crm?.realName || '').trim();
  if (!real) return false;
  return project.crm.namePublic === true || real === project.name;
}
