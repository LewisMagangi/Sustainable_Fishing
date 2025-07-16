document.addEventListener("DOMContentLoaded", function () {
  initializeAdminEnhancements();

  addStatisticsSummary();

  enhanceFormInteractions();

  addConfirmationDialogs();

  initializeTooltips();

  addKeyboardShortcuts();
});

function initializeAdminEnhancements() {
  const body = document.body;
  body.classList.add("sustainable-fishing-admin");

  const tableRows = document.querySelectorAll(".results tbody tr");
  tableRows.forEach((row) => {
    row.addEventListener("mouseenter", function () {
      this.style.backgroundColor = "#f8f9fa";
    });

    row.addEventListener("mouseleave", function () {
      this.style.backgroundColor = "";
    });
  });

  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function () {
      const submitBtn = this.querySelector(
        'input[type="submit"], button[type="submit"]'
      );
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.6";
        submitBtn.value = "Processing...";
      }
    });
  });
}

function addStatisticsSummary() {
  const changeList = document.querySelector(".change-list");
  if (changeList && !document.querySelector(".summary-stats")) {
    const summaryDiv = document.createElement("div");
    summaryDiv.className = "summary-stats";
    summaryDiv.innerHTML = `
            <h3>Quick Statistics</h3>
            <div id="stats-container">
                <div class="stat-item">
                    <div class="stat-value" id="total-items">Loading...</div>
                    <div class="stat-label">Total Items</div>
                </div>
            </div>
        `;

    const resultsDiv = document.querySelector(".results");
    if (resultsDiv) {
      resultsDiv.parentNode.insertBefore(summaryDiv, resultsDiv);

      const totalItems = document.querySelectorAll(".results tbody tr").length;
      document.getElementById("total-items").textContent = totalItems;
    }
  }
}

function enhanceFormInteractions() {
  const textareas = document.querySelectorAll("textarea");
  textareas.forEach((textarea) => {
    if (
      !textarea.nextElementSibling ||
      !textarea.nextElementSibling.classList.contains("char-count")
    ) {
      const charCount = document.createElement("div");
      charCount.className = "char-count";
      charCount.style.cssText =
        "font-size: 12px; color: #6c757d; text-align: right; margin-top: 5px;";

      const updateCount = () => {
        const count = textarea.value.length;
        charCount.textContent = `${count} characters`;

        if (count > 1000) {
          charCount.style.color = "#dc3545";
        } else if (count > 500) {
          charCount.style.color = "#fd7e14";
        } else {
          charCount.style.color = "#6c757d";
        }
      };

      textarea.addEventListener("input", updateCount);
      textarea.parentNode.insertBefore(charCount, textarea.nextSibling);
      updateCount();
    }
  });

  const inputs = document.querySelectorAll(
    "input[required], select[required], textarea[required]"
  );
  inputs.forEach((input) => {
    input.addEventListener("blur", function () {
      if (!this.value.trim()) {
        this.style.borderColor = "#dc3545";
      } else {
        this.style.borderColor = "#28a745";
      }
    });

    input.addEventListener("input", function () {
      if (this.value.trim()) {
        this.style.borderColor = "#28a745";
      }
    });
  });
}

function addConfirmationDialogs() {
  const deleteLinks = document.querySelectorAll('a[href*="delete"]');
  deleteLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      if (
        !confirm(
          "Are you sure you want to delete this item? This action cannot be undone."
        )
      ) {
        e.preventDefault();
      }
    });
  });

  const actionSelect = document.querySelector('select[name="action"]');
  if (actionSelect) {
    actionSelect.addEventListener("change", function () {
      const selectedAction = this.value;
      const destructiveActions = [
        "delete_selected",
        "deactivate_users",
        "unpublish_content",
      ];

      if (destructiveActions.includes(selectedAction)) {
        const goButton = document.querySelector(
          'button[title="Run the selected action"]'
        );
        if (goButton) {
          goButton.style.backgroundColor = "#dc3545";
          goButton.style.color = "white";
        }
      }
    });
  }
}

function initializeTooltips() {
  const statusIndicators = document.querySelectorAll(
    ".status-indicator, [data-tooltip]"
  );
  statusIndicators.forEach((element) => {
    element.addEventListener("mouseenter", function (e) {
      const tooltip = document.createElement("div");
      tooltip.className = "custom-tooltip";
      tooltip.textContent =
        this.getAttribute("data-tooltip") || this.textContent;
      tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                max-width: 200px;
            `;

      document.body.appendChild(tooltip);

      const rect = this.getBoundingClientRect();
      tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + "px";
      tooltip.style.left =
        rect.left + (rect.width - tooltip.offsetWidth) / 2 + "px";
    });

    element.addEventListener("mouseleave", function () {
      const tooltip = document.querySelector(".custom-tooltip");
      if (tooltip) {
        tooltip.remove();
      }
    });
  });
}

function addKeyboardShortcuts() {
  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.key === "s") {
      e.preventDefault();
      const saveButton = document.querySelector(
        'input[name="_save"], button[name="_save"]'
      );
      if (saveButton) {
        saveButton.click();
      }
    }

    if (e.ctrlKey && e.key === "Enter") {
      e.preventDefault();
      const saveAndContinueButton = document.querySelector(
        'input[name="_continue"], button[name="_continue"]'
      );
      if (saveAndContinueButton) {
        saveAndContinueButton.click();
      }
    }

    if (e.key === "Escape") {
      const cancelButton = document.querySelector(
        'a[href*="changelist"], .cancel-link'
      );
      if (cancelButton && !document.querySelector(".custom-tooltip")) {
        window.location.href = cancelButton.href;
      }
    }
  });
}

function showNotification(message, type = "success") {
  const notification = document.createElement("div");
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 4px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;

  if (type === "success") {
    notification.style.backgroundColor = "#28a745";
  } else if (type === "error") {
    notification.style.backgroundColor = "#dc3545";
  } else if (type === "warning") {
    notification.style.backgroundColor = "#ffc107";
    notification.style.color = "#212529";
  }

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease-out";
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 3000);
}

function updateStatistics() {
  console.log("Updating statistics...");
}

const style = document.createElement("style");
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
`;
document.head.appendChild(style);

window.SustainableFishingAdmin = {
  showNotification,
  updateStatistics,
};
