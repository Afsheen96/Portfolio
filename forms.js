// Contact and Hire Me forms.
// Messages are delivered by Formspree (the form service already used on this
// site, set in each form's "action"). With JavaScript the form is sent in the
// background and a message is shown on the page; without JavaScript the
// browser posts the form to Formspree normally.
(() => {
  const forms = document.querySelectorAll('form[data-ajax-form]');

  function setStatus(form, type, text) {
    const status = form.querySelector('.form-status');
    if (!status) return;
    status.className = `form-status ${type}`;
    status.textContent = text;
  }

  // Email must be lowercase (kept from the original site's validation).
  function validateEmail(form) {
    const email = form.querySelector('input[type="email"]');
    if (!email) return true;
    if (email.value !== email.value.toLowerCase()) {
      email.setCustomValidity('*Email must be in lowercase!');
      return false;
    }
    email.setCustomValidity('');
    return true;
  }

  forms.forEach((form) => {
    const key = form.dataset.draftKey;
    const selector = 'input[name]:not([type="hidden"]):not(.hp-field), textarea[name], select[name]';
    const fields = Array.from(form.querySelectorAll(selector));

    // ---- keep an unsent draft in this browser (local storage) ----
    const saveDraft = () => {
      if (!key) return;
      const data = {};
      fields.forEach((f) => {
        if (f.type === 'radio') {
          if (f.checked) data[f.name] = f.value;
        } else {
          data[f.name] = f.value;
        }
      });
      try {
        localStorage.setItem(key, JSON.stringify(data));
      } catch (e) { /* storage unavailable */ }
    };
    try {
      const saved = key && JSON.parse(localStorage.getItem(key));
      if (saved) {
        fields.forEach((f) => {
          if (!(f.name in saved)) return;
          if (f.type === 'radio') f.checked = f.value === saved[f.name];
          else f.value = saved[f.name];
        });
      }
    } catch (e) { /* ignore broken drafts */ }
    form.addEventListener('input', saveDraft);
    form.addEventListener('change', saveDraft);

    // ---- live field feedback ----
    fields.forEach((f) => {
      f.addEventListener('blur', () => {
        if (f.type === 'email') validateEmail(form);
        if (f.value || f.type === 'radio') f.closest('.field')?.classList.toggle('invalid', !f.checkValidity());
      });
      f.addEventListener('input', () => {
        if (f.type === 'email') validateEmail(form);
        if (f.checkValidity()) f.closest('.field')?.classList.remove('invalid');
      });
    });

    // ---- submit ----
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      validateEmail(form);
      let firstBad = null;
      fields.forEach((f) => {
        const ok = f.checkValidity();
        f.closest('.field')?.classList.toggle('invalid', !ok);
        if (!ok && !firstBad) firstBad = f;
      });
      if (firstBad) {
        setStatus(form, 'error', firstBad.validationMessage || 'Please check the highlighted fields.');
        firstBad.focus();
        return;
      }

      const button = form.querySelector('.form-submit');
      button.disabled = true;
      button.classList.add('is-loading');
      setStatus(form, 'info', 'Sending your message...');

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' },
        });
        if (!response.ok) throw new Error(`Status ${response.status}`);
        form.reset();
        try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
        form.classList.add('is-sent');
        setStatus(form, 'success', form.id === 'hireform'
          ? 'Thank you! Your project inquiry has been sent. I will reply by email soon.'
          : 'Thank you! Your message has been sent. I will get back to you soon.');
      } catch (err) {
        setStatus(form, 'error', 'Sorry, the message could not be sent right now. Please try again in a moment, or reach me on LinkedIn.');
      } finally {
        button.disabled = false;
        button.classList.remove('is-loading');
      }
    });
  });
})();
