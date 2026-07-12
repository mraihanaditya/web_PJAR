/* =========================================================
   Socket Web Platform — app.js
   Vanilla JavaScript only, no external libraries.
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  initHeaderScroll();
  initPasswordToggle();
  initRipple();
  initFlashToasts();
  initUploadForm();
});

/* ---------------------------------------------------------
   Header scroll state
--------------------------------------------------------- */
function initHeaderScroll() {
  const header = document.getElementById('siteHeader');
  if (!header) return;

  const onScroll = () => {
    if (window.scrollY > 12) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ---------------------------------------------------------
   Show / Hide password
--------------------------------------------------------- */
function initPasswordToggle() {
  document.querySelectorAll('.toggle-pass').forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const input = document.getElementById(targetId);
      if (!input) return;

      const icon = btn.querySelector('i');
      const isHidden = input.type === 'password';

      input.type = isHidden ? 'text' : 'password';
      if (icon) {
        icon.classList.toggle('fa-eye', !isHidden);
        icon.classList.toggle('fa-eye-slash', isHidden);
      }
    });
  });
}

/* ---------------------------------------------------------
   Ripple effect on .ripple buttons
--------------------------------------------------------- */
function initRipple() {
  document.querySelectorAll('.ripple').forEach((el) => {
    el.addEventListener('click', function (e) {
      const rect = this.getBoundingClientRect();
      const circle = document.createElement('span');
      const size = Math.max(rect.width, rect.height);

      circle.className = 'ripple-circle';
      circle.style.width = circle.style.height = `${size}px`;
      circle.style.left = `${e.clientX - rect.left - size / 2}px`;
      circle.style.top = `${e.clientY - rect.top - size / 2}px`;

      this.appendChild(circle);
      window.setTimeout(() => circle.remove(), 600);
    });
  });
}

/* ---------------------------------------------------------
   Flask flash messages -> Toast notifications
--------------------------------------------------------- */
function initFlashToasts() {
  const flashData = document.getElementById('flashData');
  const container = document.getElementById('toastContainer');
  if (!flashData || !container) return;

  const messages = flashData.querySelectorAll('[data-flash]');
  messages.forEach((node, index) => {
    const text = node.textContent.trim();
    if (!text) return;

    window.setTimeout(() => {
      showToast(text, classifyFlash(text));
    }, index * 180);
  });
}

function classifyFlash(text) {
  const lower = text.toLowerCase();
  const successHints = ['berhasil', 'success', 'online'];
  const errorHints = ['gagal', 'error', 'tidak', 'salah'];

  if (successHints.some((w) => lower.includes(w))) return 'success';
  if (errorHints.some((w) => lower.includes(w))) return 'error';
  return 'info';
}

function showToast(message, type = 'info', duration = 4500) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const icons = {
    success: 'fa-circle-check',
    error: 'fa-circle-exclamation',
    info: 'fa-circle-info',
  };

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <i class="fa-solid ${icons[type] || icons.info} toast-icon"></i>
    <span class="toast-message"></span>
    <button type="button" class="toast-close" aria-label="Tutup notifikasi">
      <i class="fa-solid fa-xmark"></i>
    </button>
  `;
  toast.querySelector('.toast-message').textContent = message;

  const close = () => {
    toast.classList.add('hide');
    window.setTimeout(() => toast.remove(), 320);
  };

  toast.querySelector('.toast-close').addEventListener('click', close);
  container.appendChild(toast);

  window.setTimeout(close, duration);
}

/* ---------------------------------------------------------
   Upload form: drag & drop, preview, fake progress
--------------------------------------------------------- */
function initUploadForm() {
  const form = document.getElementById('uploadForm');
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const filePreview = document.getElementById('filePreview');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const fileRemove = document.getElementById('fileRemove');
  const progressTrack = document.getElementById('progressTrack');
  const progressFill = document.getElementById('progressFill');
  const uploadBtn = document.getElementById('uploadBtn');

  if (!form || !dropzone || !fileInput) return;

  ['dragenter', 'dragover'].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files && files.length) {
      fileInput.files = files;
      updatePreview(files[0]);
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files[0]) {
      updatePreview(fileInput.files[0]);
    }
  });

  if (fileRemove) {
    fileRemove.addEventListener('click', () => {
      fileInput.value = '';
      filePreview.hidden = true;
      dropzone.hidden = false;
    });
  }

  function updatePreview(file) {
    if (!filePreview || !fileName || !fileSize) return;
    fileName.textContent = file.name;
    fileSize.textContent = formatBytes(file.size);
    filePreview.hidden = false;
    dropzone.hidden = true;
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 KB';
    const units = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    const value = bytes / Math.pow(1024, i);
    return `${value.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
  }

  form.addEventListener('submit', () => {
    if (!fileInput.files || !fileInput.files[0]) return;

    if (uploadBtn) {
      uploadBtn.disabled = true;
      uploadBtn.style.opacity = '0.7';
      uploadBtn.querySelector('span').textContent = 'Uploading...';
    }

    if (progressTrack && progressFill) {
      progressTrack.hidden = false;
      let progress = 0;
      const interval = window.setInterval(() => {
        progress = Math.min(progress + Math.random() * 18, 92);
        progressFill.style.width = `${progress}%`;
      }, 220);

      window.addEventListener('beforeunload', () => window.clearInterval(interval));
    }
    // Native form submission proceeds to the existing /upload endpoint.
  });
}