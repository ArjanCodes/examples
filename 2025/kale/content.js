// Utility functions
const sendMessage = async (message) => {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(message, (response) => {
      if (chrome.runtime.lastError) {
        return reject(new Error(chrome.runtime.lastError.message));
      }
      if (response?.error) {
        return reject(new Error(response.error));
      }
      resolve(response);
    });
  });
};

const isAffiliated = async () => sendMessage({ type: "IS_AFFILIATED" });

// DOM Manipulation
const createPopup = (isAffiliated, onApplyClick) => {
  const popup = document.createElement("div");
  popup.id = "discount-popup";
  popup.innerHTML = `
    <div class="header">
      <div class="logo">&#x1D4A6;</div>
      <div id="close-btn">X</div>
    </div>
    <div class="content">
      <div class="content-left-body">
        <img id="icon" src="https://889r7vs5ma.ufs.sh/f/lB9nBfMEwa3m2tA7F1odSn4gaWt3YBr1UjzcQvIeNXuy7C8l" alt="Kale Icon" />
      </div>
      <div class="content-body">
        <h1>
          ${!isAffiliated ? "<p>We found a coupon!</p>" : ""}
          ${isAffiliated ? "<p>Your purchase is Supporting a creator</p>" : ""}
        </h1>
        ${
          !isAffiliated &&
          "<p>Select whether you'd like to support Kale or a creator.</p>"
        }
        <div class="buttons">
          ${
            !isAffiliated
              ? '<button id="apply-random-discounts" class="apply-btn">Add coupon and support creator</button>'
              : ""
          }
          ${
            !isAffiliated
              ? '<button id="apply-kale-discounts" class="apply-btn">Add coupon and support Kale</button>'
              : ""
          }
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(popup);

  document.getElementById("close-btn").onclick = () =>
    document.body.removeChild(popup);

  if (!isAffiliated) {
    document.getElementById("apply-random-discounts").onclick = async () => {
      await onApplyClick("random");
      updatePopup(true);
    };

    document.getElementById("apply-kale-discounts").onclick = async () => {
      await onApplyClick("kale");
      updatePopup(false);
    };
  }
};

const updatePopup = (isAffiliated) => {
  const popup = document.getElementById("discount-popup");
  if (popup) {
    popup.querySelector(".content-body").innerHTML = `
      <h1><p>Your purchase is ${
        isAffiliated ? "affiliated" : "not affiliated"
      }</p></h1>
    `;
  }
};

const setLoading = () => {
  const popup = document.getElementById("discount-popup");
  if (popup) {
    popup.querySelector(".content-body").innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle fill="#142d45" stroke="#142d45" stroke-width="7.5" r="7.5" cx="20" cy="32.5">
    <animate attributeName="cy" calcMode="spline" dur="2s" values="32.5;67.5;32.5" keySplines=".5 0 .5 1;.5 0 .5 1" repeatCount="indefinite" begin="-.4s"></animate>
  </circle>
  <circle fill="#142d45" stroke="#142d45" stroke-width="7.5" r="7.5" cx="50" cy="32.5">
    <animate attributeName="cy" calcMode="spline" dur="2s" values="32.5;67.5;32.5" keySplines=".5 0 .5 1;.5 0 .5 1" repeatCount="indefinite" begin="-.2s"></animate>
  </circle>
  <circle fill="#142d45" stroke="#142d45" stroke-width="7.5" r="7.5" cx="80" cy="32.5">
    <animate attributeName="cy" calcMode="spline" dur="2s" values="32.5;67.5;32.5" keySplines=".5 0 .5 1;.5 0 .5 1" repeatCount="indefinite" begin="0s"></animate>
  </circle>
</svg>

      `;
  }
};

const checkIfCheckoutPage = async () => {
  if (document.body.innerText.includes("Checkout")) {
    return true;
  }

  const href = window.location.href;

  if (
    href.includes("checkout") ||
    href.includes("cart") ||
    href.includes("order")
  ) {
    return true;
  }

  return false;
};

// Get affilate options

// Main
(async () => {
  const isCheckoutPage = await checkIfCheckoutPage();

  if (!isCheckoutPage) return;

  const affiliated = await isAffiliated();

  createPopup(affiliated, async (action) => {
    const affiliated_message = await sendMessage({
      support: action,
      type: "AFFILIATE_PURCHASE",
    });

    // Render spinner
    if (affiliated_message.response === "Affiliate purchase completed") {
      setLoading();
    }

    const tab_closing = await sendMessage({
      type: "CLOSE_TAB",
      tab_id: affiliated_message.tab_id,
    });

    // Refresh the page
    window.location.reload();
  });
})();
