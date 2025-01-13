const affiliateTracking = {
  aff_id: "12345", // Unique identifier for the affiliate
  affiliate_id: "abc123", // Alternative affiliate ID
  ref: "user123", // Referring affiliate
  ref_id: "78910", // Referral ID
  utm_source: "affiliate_network", // Source of traffic
  utm_medium: "cpa", // Medium of the traffic
  utm_campaign: "winter_promo", // Campaign name
  utm_term: "special_offer", // Keyword or term
  utm_content: "banner1", // Differentiates ads
  partner_id: "partner987", // Partner or affiliate program ID
  tracking_id: "track5678", // General tracking ID
  click_id: "click1234", // Unique click identifier
  sub_id: "subAffiliate001", // Sub-affiliate ID
  pid: "program456", // Partner program ID
  sid: "session789", // Session ID
  aid: "affiliateX", // Affiliate ID
  cid: "campaign001", // Campaign ID
  ad_id: "ad5678", // Ad-specific identifier
  offer_id: "offer2025", // Specific offer identifier
  pub_id: "pub999", // Publisher ID
  source: "newsletter", // Generic source
  fbclid: "fb123abc", // Facebook click ID
  gclid: "google123abc", // Google Ads click ID
  tid: "tracking987", // General tracking parameter
};

const DISCOUNTS = {
  "https://www.newegg.com/intel-core-i7-12700k-core-i7-12th-gen-alder-lake-lga-1700-desktop-processor/p/N82E16819118343":
    "SAVE10",
};

function getCurrentTab() {
  return new Promise((resolve, reject) => {
    let queryOptions = { active: true, lastFocusedWindow: true };
    chrome.tabs.query(queryOptions, ([tab]) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else if (!tab) {
        reject(new Error("No active tab found."));
      } else {
        resolve(tab);
      }
    });
  });
}

// UTM tag logic
function extractUTMTags(url) {
  try {
    const urlParams = new URLSearchParams(new URL(url).search);
    const utmTags = {};
    for (const [key, value] of urlParams) {
      if (key.startsWith("utm_")) {
        utmTags[key] = value;
      }
    }
    return utmTags;
  } catch (error) {
    console.error("Error parsing URL:", error);
    return null;
  }
}

function generateAffilateLinkUrl(url, tracking = affiliateTracking) {
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

function removeUTMTags(url) {
  try {
    const urlObj = new URL(url);
    urlObj.searchParams.delete("utm_source");
    urlObj.searchParams.delete("utm_medium");
    urlObj.searchParams.delete("utm_campaign");
    urlObj.searchParams.delete("utm_term");
    urlObj.searchParams.delete("utm_content");
    return urlObj.href;
  } catch (error) {
    console.error("Error parsing URL:", error);
    return null;
  }
}

async function getCurrentUTMTags() {
  try {
    const tab = await getCurrentTab();
    const utmTags = extractUTMTags(tab.url);
    console.log("currentUrl", tab.url);
    console.log("tags", utmTags);
    return utmTags;
  } catch (error) {
    console.error("Error getting UTM tags:", error);
    return null;
  }
}

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

function closeTab(tab) {
  return new Promise((resolve, reject) => {
    chrome.tabs.remove(tab.id, function () {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve();
      }
    });
  });
}

async function findDiscountCode(utm) {
  const { discounts } = await getDiscounts();
  const utmTags = await getCurrentUTMTags();
  if (!utmTags) {
    return null;
  }

  for (const discount of discounts) {
    if (utmTags.utm_campaign === discount.code) {
      return discount;
    }
  }

  return null;
}

async function getDiscounts() {
  const discounts = DISCOUNTS;
  return { discounts };
}

async function injectQueryParameters(url, query_parameters) {
  const urlObj = new URL(url);
  for (const [key, value] of Object.entries(query_parameters)) {
    urlObj.searchParams.set(key, value);
  }
  return urlObj.href;
}

chrome.runtime.onMessage.addListener(async function (
  request,
  sender,
  sendResponse
) {
  const currentTab = await getCurrentTab();

  // const newUrl = await updateUTMTags(currentTab.url, {
  //   utm_campaign: "kale",
  //   utm_source: "kale",
  // });

  const newUrl = generateAffilateLinkUrl(currentTab.url);

  const tab = await createTab(newUrl);

  console.log(
    sender.tab
      ? "from a content script:" + sender.tab.url
      : "from the extension"
  );
  if (request.greeting === "hello") sendResponse({ farewell: "goodbye" });
});

document.addEventListener("DOMContentLoaded", async () => {
  const { discounts } = await getDiscounts();

  const numberOfDiscounts = discounts.length;

  const element = document.getElementById("number-of-discount");

  element.innerText = numberOfDiscounts;
});

// document.addEventListener("DOMContentLoaded", async () => {
//   const couponsDiv = document.getElementById("coupons");

//   // Send a message to the content script
//   chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
//     if (tab.id) {
//       chrome.tabs.sendMessage(tab.id, { action: "findCoupons" }, (response) => {
//         if (response && response.coupons && response.coupons.length > 0) {
//           couponsDiv.innerHTML = `<ul>${response.coupons
//             .map((coupon) => `<li>${coupon}</li>`)
//             .join("")}</ul>`;
//         } else {
//           couponsDiv.textContent = "No coupons found on this page.";
//         }
//       });
//     }
//   });
// });

document.getElementById("close-btn").onclick = async function () {
  window.close();
};

document.getElementById("apply-discounts").onclick = async function () {
  const currentTab = await getCurrentTab();

  // const newUrl = await updateUTMTags(currentTab.url, {
  //   utm_campaign: "kale",
  //   utm_source: "kale",
  // });

  const newUrl = generateAffilateLinkUrl(currentTab.url);

  const tab = await createTab(newUrl);

  await setTimeout(() => closeTab(tab), 3000);
};
