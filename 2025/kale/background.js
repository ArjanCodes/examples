const affiliateLinks = [
  {
    service: "nordvpn",
    influencer: "pewdiepie",
    link: "https://nordvpn.com/pricing/creator/?coupon=pewdiepie",
  },
  {
    service: "nordvpn",
    influencer: "mrbeast",
    link: "https://nordvpn.com/creator/entertainment/?coupon=mrbeastgaming",
  },
  {
    service: "nordvpn",
    influencer: "oversimplified",
    link: "https://nordvpn.com/creator/education/?coupon=oversimplified",
  },
  {
    service: "nordvpn",
    influencer: "johnnyharris",
    link: "https://nordvpn.com/creator/education/?coupon=johnnyharris",
  },
  {
    service: "privateinternetaccess",
    influencer: "linustechtips",
    link: "https://www.privateinternetaccess.com/linus-tech-tips?coupon=linus1",
  },
];

const services = {
  nordvpn: ["nordvpn", "nordcheckout"],
  privateinternetaccess: ["privateinternetaccess"],
};

async function findServiceByUrl(url) {
  for (const [key, substrings] of Object.entries(services)) {
    if (substrings.some((substring) => url.includes(substring))) {
      return key;
    }
  }
  return null;
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

const getRandomAffiliateLink = (service) => {
  const serviceLinks = affiliateLinks.filter(
    (link) => link.service === service
  );

  if (!serviceLinks.length) {
    throw new Error(`No affiliate links available for service: ${service}`);
  }

  return serviceLinks.at(Math.floor(Math.random() * serviceLinks.length));
};

const kaleAffiliate = {
  aff_id: "kale", // Unique identifier for the affiliate
  affiliate_id: "kale123", // Alternative affiliate ID
  ref: "kale", // Referring affiliate
  ref_id: "kale", // Referral ID
  utm_source: "kale", // Source of traffic
  utm_medium: "kale", // Medium of the traffic
  utm_campaign: "kale", // Campaign name
  utm_term: "kale", // Keyword or term
  utm_content: "kale", // Differentiates ads
  partner_id: "kale", // Partner or affiliate program ID
  tracking_id: "kale", // General tracking ID
  click_id: "kale", // Unique click identifier
  sub_id: "kale", // Sub-affiliate ID
  pid: "kale", // Partner program ID
  sid: "kale", // Session ID
  aid: "kale", // Affiliate ID
  cid: "kale", // Campaign ID
  ad_id: "kale", // Ad-specific identifier
  offer_id: "kale", // Specific offer identifier
  pub_id: "kale", // Publisher ID
  source: "kale", // Generic source
  fbclid: "kale", // Facebook click ID
  gclid: "kale", // Google Ads click ID
  tid: "kale", // General tracking parameter
};

const affiliateCookies = [
  "affiliate",
  "affiliate_id",
  "ref",
  "ref_id",
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_term",
  "utm_content",
  "partner_id",
  "tracking_id",
  "click_id",
  "sub_id",
  "ad_id",
  "offer_id",
  "pub_id",
  "source",
  "NV_MC_LC",
  "NV_MC_HOWL",
  "coupon",
  "coupon_",
  "coupon_nordvpn",
];

function createTab(url, active = false) {
  return new Promise((resolve, reject) => {
    chrome.tabs.create({ url, active }, function (tab) {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(tab); // Resolve with the tab ID
      }
    });
  });
}

function generateAffilateLinkUrl(url, tracking = kaleAffiliate) {
  try {
    const urlObj = new URL(url);
    for (const [key, value] of Object.entries(tracking)) {
      urlObj.searchParams.has(key) && urlObj.searchParams.set(key, value);
    }
    return urlObj.href;
  } catch (error) {
    console.error("Error parsing URL:", error);
    return null;
  }
}

async function getCurrentTab() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (chrome.runtime.lastError) {
        return reject(chrome.runtime.lastError);
      }
      if (tabs.length === 0) {
        return reject(new Error("No active tab found"));
      }
      resolve(tabs[0]);
    });
  });
}

// Close tab
async function closeTab(tab_id) {
  return new Promise((resolve, reject) => {
    chrome.tabs.remove(tab_id, function () {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve();
      }
    });
  });
}

async function getCurrentURL(_request, _sender, sendResponse) {
  try {
    const tab = await getCurrentTab(); // Assuming this function fetches the current tab
    const response = { response: tab.url };

    sendResponse(response); // Send the response back to the content script
  } catch (error) {
    console.error("Error fetching tab URL:", error);
    sendResponse({ error: error.message });
  }
}

async function getDomain(url) {
  try {
    return new URL(url).hostname;
  } catch (error) {
    console.error("Error parsing URL:", error);
    return null;
  }
}

async function getCookiesForCurrentTab() {
  const tab = await getCurrentTab();
  if (!tab?.url) {
    throw new Error("No active tab or URL found");
  }

  var domain = await getDomain(tab.url);

  // If domain is a subdomain, remove the subdomain part
  // Example: "www.example.com" -> "example.com"
  const parts = domain.split(".");
  if (parts.length > 2) {
    domain = parts.slice(1).join(".");
  }

  return new Promise((resolve, reject) => {
    chrome.cookies.getAll({ domain }, (cookies) => {
      if (chrome.runtime.lastError) {
        return reject(new Error(chrome.runtime.lastError.message));
      }
      resolve(cookies);
    });
  });
}

async function getTab(tab_id) {
  return new Promise((resolve, reject) => {
    chrome.tabs.get(tab_id, (tab) => {
      if (chrome.runtime.lastError) {
        return reject(new Error(chrome.runtime.lastError.message));
      }
      resolve(tab);
    });
  });
}

async function getCookiesFromTab(tab_id) {
  const tab = await getTab(tab_id);

  return new Promise((resolve, reject) => {
    chrome.cookies.getAll({ url: tab.url || tab.pendingUrl }, (cookies) => {
      if (chrome.runtime.lastError) {
        return reject(new Error(chrome.runtime.lastError.message));
      }
      resolve(cookies);
    });
  });
}

async function isAffliated() {
  const cookies = await getCookiesForCurrentTab();

  const filteredCookies = cookies.filter((cookie) =>
    affiliateCookies.includes(cookie.name)
  );

  if (filteredCookies.length === 0) {
    return false;
  }

  if (!filteredCookies) {
    return false;
  }

  return true;
}

function timeout(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function finishLoading(tabId) {
  await new Promise((resolve) => {
    const listener = (updatedTabId, changeInfo) => {
      if (updatedTabId === tabId && changeInfo.status === "complete") {
        chrome.tabs.onUpdated.removeListener(listener);
        resolve();
      }
    };

    chrome.tabs.onUpdated.addListener(listener);
  });

  await new Promise((resolve) => setTimeout(resolve, 2000));

  // Close the tab
  chrome.tabs.remove(tabId);
}

async function affiliatePurchase(support) {
  const tab = await getCurrentTab();

  if (support === "kale") {
    const kale_url = generateAffilateLinkUrl(tab.url);
    const kale_tab = await createTab(kale_url, false);
    return { response: "Affiliate purchase completed", tab_id: kale_tab.id };
  }
  const service = await findServiceByUrl(tab.url);

  console.log("service", service);

  const affiliateLink = await getRandomAffiliateLink(service);

  console.log("affiliateLink", affiliateLink);

  if (!affiliateLink) {
    return { response: "No affiliate link found" };
  }

  const newTab = await createTab(affiliateLink.link, false);

  if (!service) {
    return { response: "No service found" };
  }

  const cookies = await getCookiesFromTab(newTab.id);

  // Filter out cookies that are not related to affiliate tracking
  const filteredCookies = cookies.filter((cookie) =>
    affiliateCookies.includes(cookie.name)
  );

  console.log("cookies", filteredCookies);
  return {
    text: "Affiliate purchase completed",
    influencer: affiliateLink.influencer || "kale",
    tab_id: newTab.id,
    cookies: filteredCookies,
  };
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "IS_AFFILIATED") {
    isAffliated().then((affiliated) => {
      sendResponse(affiliated);
    });
    return true;
  }
  if (request.type === "AFFILIATE_PURCHASE") {
    affiliatePurchase(request.support).then(async (response) => {
      if (!response) {
        return sendResponse({ response: "No affiliate link found" });
      }

      if (response.response === "No service found") {
        return sendResponse({ response: "No service found" });
      }

      const { cookies, tab_id } = response;
      const tab = await getCurrentTab(); // Assuming this function fetches the current tab

      const domain = await getDomain(tab.url);

      cookies.forEach((cookie) => {
        // Create a cleaned version of the cookie object
        const cleanedCookie = Object.fromEntries(
          Object.entries({
            ...cookie,
            hostOnly: undefined,
            session: undefined,
            storeId: undefined,
          }).filter(([_, value]) => value !== undefined) // Filter out undefined values
        );

        // Set the cleaned cookie in the browser
        chrome.cookies.set({
          ...cleanedCookie,
          domain,
          url: "https://nordcheckout.com",
        });
      });

      // Send the updated response
      sendResponse({
        response: "Affiliate purchase completed",
        tab_id,
      });
    });

    return true;
  }
  if (request.type === "GET_AFFILIATE_OPTIONS") {
    getAffiliateOptions(request.service).then((response) => {
      sendResponse(response);
    });
    return true;
  }

  if (request.type === "CLOSE_TAB") {
    finishLoading(request.tab_id).then(() => {
      sendResponse({ response: "Loading finished" });
    });
    return true;
  }
});
