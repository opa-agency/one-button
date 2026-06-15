(() => {
  const MESSAGE_DURATION = 2000;

  function toInt(value, fallback) {
    const parsed = parseInt(value, 10);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function getOriginalLabel(button) {
    if (!button.dataset.shareOriginalLabel) {
      button.dataset.shareOriginalLabel = button.textContent.trim();
    }
    return button.dataset.shareOriginalLabel;
  }

  function setButtonLabel(button, label) {
    if (typeof label === "string" && label.length) {
      button.textContent = label;
    }
  }

  function restoreLabel(button) {
    setButtonLabel(button, getOriginalLabel(button));
  }

  function showTemporaryLabel(button, label, duration) {
    setButtonLabel(button, label);
    const delay = toInt(button.dataset.shareMessageDuration, duration);
    window.setTimeout(() => {
      restoreLabel(button);
      button.removeAttribute("aria-busy");
    }, delay);
  }

  function buildShareText(text, url) {
    const cleanText = (text || "").trim();
    const cleanUrl = (url || "").trim();
    if (cleanText && cleanUrl) {
      return `${cleanText}\n${cleanUrl}`;
    }
    return cleanText || cleanUrl || "";
  }

  async function copyToClipboard(value) {
    const text = value || "";
    if (!text) {
      return;
    }

    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      try {
        await navigator.clipboard.writeText(text);
        return;
      } catch (error) {
        // fallback continues
      }
    }

    return new Promise((resolve) => {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
      } catch (ignore) {
        // swallow
      }
      document.body.removeChild(textarea);
      resolve();
    });
  }

  function fileNameFromUrl(url, fallback) {
    if (!url) {
      return fallback;
    }
    try {
      const { pathname } = new URL(url, window.location.href);
      const name = pathname.split("/").filter(Boolean).pop();
      return name || fallback;
    } catch (error) {
      return fallback;
    }
  }

  async function fetchImageFile(imageUrl, fallbackName) {
    const response = await fetch(imageUrl, { credentials: "omit", cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Image response not ok (${response.status})`);
    }
    const blob = await response.blob();
    const fileName = fileNameFromUrl(imageUrl, fallbackName);
    const options = { type: blob.type || "image/png", lastModified: Date.now() };
    if (typeof File === "function") {
      return new File([blob], fileName, options);
    }
    const fallbackFile = blob;
    fallbackFile.name = fileName;
    return fallbackFile;
  }

  function isAbortError(error) {
    if (!error) {
      return false;
    }
    return error.name === "AbortError" || error.name === "NotAllowedError" || /cancel/i.test(error.message || "");
  }

  async function shareWithImage(button, shareData, imageUrl) {
    try {
      const imageFile = await fetchImageFile(imageUrl, "share-image.png");
      if (navigator.canShare && navigator.canShare({ files: [imageFile] })) {
        await navigator.share({ ...shareData, files: [imageFile] });
        return true;
      }
    } catch (error) {
      console.warn("Image sharing failed, falling back to text", error);
    }
    return false;
  }

  async function handleShare(button) {
    const title = button.dataset.shareTitle || document.title || "";
    const text = button.dataset.shareText || "";
    const url = button.dataset.shareUrl || window.location.href;
    const imageUrl = button.dataset.shareImage || "";

    const loadingLabel = button.dataset.shareLoading || "Se pregătește...";
    const successLabel = button.dataset.shareSuccess || "Trimis";
    const fallbackLabel = button.dataset.shareFallback || "Copiat";
    const errorLabel = button.dataset.shareError || "Nu am putut partaja";

    const shareText = buildShareText(text, url);
    const originalLabel = getOriginalLabel(button);

    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    setButtonLabel(button, loadingLabel);

    const shareData = {
      title: title || undefined,
      text: text ? text : undefined,
      url: url || undefined,
    };

    try {
      if (navigator.share) {
        if (imageUrl && navigator.canShare) {
          const shared = await shareWithImage(button, shareData, imageUrl);
          if (shared) {
            showTemporaryLabel(button, successLabel, MESSAGE_DURATION);
            return;
          }
        }

        await navigator.share(shareData);
        showTemporaryLabel(button, successLabel, MESSAGE_DURATION);
        return;
      }

      await copyToClipboard(shareText);
      showTemporaryLabel(button, fallbackLabel, MESSAGE_DURATION);
    } catch (error) {
      if (isAbortError(error)) {
        restoreLabel(button);
        button.removeAttribute("aria-busy");
        return;
      }

      console.error("Share failed", error);

      try {
        await copyToClipboard(shareText);
        showTemporaryLabel(button, fallbackLabel, MESSAGE_DURATION);
      } catch (copyError) {
        console.error("Fallback copy failed", copyError);
        showTemporaryLabel(button, errorLabel, MESSAGE_DURATION);
      }
    } finally {
      button.disabled = false;
    }
  }

  function initButton(button) {
    if (button.dataset.shareInitialized === "true") {
      return;
    }
    button.dataset.shareInitialized = "true";
    button.addEventListener("click", () => {
      void handleShare(button);
    });
  }

  function init() {
    const buttons = document.querySelectorAll("[data-share-button]");
    buttons.forEach(initButton);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
