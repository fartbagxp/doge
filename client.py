from urllib.parse import urlencode
from curl_cffi import requests

class DogeClient:
  def __init__(self, base_url="https://api.doge.gov"):
    self.base_url = base_url
    self.session = requests.Session()

  def _get_paginated(self, path, params=None):
    MAX_PER_PAGE = 500
    all_items = []
    page = 1
    while True:
      q = params.copy() if params else {}
      q["page"] = page
      q["per_page"] = MAX_PER_PAGE
      q["sort_by"] = "date"
      url = f"{self.base_url}{path}?{urlencode(q)}"
      resp = self.session.get(url)
      print(resp.status_code, url)
      data = resp.json()
      if not data.get("success"):
        break
      results = list(data.get("result", {}).values())[0]
      all_items.extend(results)
      if len(results) < MAX_PER_PAGE:
        break
      page += 1
    return all_items

  def get_grant_savings(self, **kwargs):
    return self._get_paginated("/savings/grants", kwargs)

  def get_contract_savings(self, **kwargs):
    return self._get_paginated("/savings/contracts", kwargs)

  def get_lease_savings(self, **kwargs):
    return self._get_paginated("/savings/leases", kwargs)

  def get_payments(self, **kwargs):
    return self._get_paginated("/payments", kwargs)

  def get_payments_statistics(self, **kwargs):
    return self._get_paginated("/payments/statistics", kwargs)