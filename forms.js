// Contact and Hire Me forms.
// Messages are emailed to Afsheen's Gmail by FormSubmit (formsubmit.co, set in
// each form's "action"). With JavaScript the form is sent in the background
// and a message is shown on the page; without JavaScript the browser posts the
// form to FormSubmit normally and comes back here with ?sent=1.
(() => {
  const forms = document.querySelectorAll('form[data-ajax-form]');

  function setStatus(form, type, text) {
    const status = form.querySelector('.form-status');
    if (!status) return;
    status.className = `form-status ${type}`;
    status.textContent = text;
  }

  // Shown when the form service is down: a mailto link with the visitor's
  // message already filled in, sent to the address in config.js.
  function showEmailFallback(form) {
    const status = form.querySelector('.form-status');
    const to = ((window.SITE_CONFIG || {}).email || '').trim();
    if (!status) return;
    status.className = 'form-status error';
    status.textContent = 'Sorry, the form could not be sent right now. ';
    if (!to) {
      status.append('Please try again in a moment.');
      return;
    }
    const data = new FormData(form);
    const lines = [];
    data.forEach((value, name) => {
      if (name.charAt(0) !== '_' && name !== 'form_type' && String(value).trim() && value !== 'No package selected') lines.push(`${name.replace(/_/g, ' ')}: ${value}`);
    });
    const subject = data.get('subject') || (form.id === 'hireform' ? 'Project inquiry' : 'Hello Afsheen');
    const link = document.createElement('a');
    link.href = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
    link.textContent = `Email me directly at ${to}`;
    status.append(link, ' (your message is already filled in).');
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
    // Came back from FormSubmit without JavaScript.
    const key = form.dataset.draftKey;
    if (/[?&]sent=1/.test(window.location.search)) {
      setStatus(form, 'success', 'Thank you! Your message has been sent. I will reply within 24 hours.');
      try { if (key) localStorage.removeItem(key); } catch (e) { /* ignore */ }
    }
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
        const response = await fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' },
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || String(result.success) !== 'true') {
          throw new Error(result.message || `Status ${response.status}`);
        }
        form.reset();
        try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
        form.classList.add('is-sent');
        setStatus(form, 'success', form.id === 'hireform'
          ? 'Thank you! Your project inquiry has been sent. I will reply by email within 24 hours.'
          : 'Thank you! Your message has been sent. I will reply within 24 hours.');
      } catch (err) {
        // The form service could not be reached or refused the message. Keep
        // the draft and offer a ready-to-send email instead, so nothing is lost.
        console.warn('Form could not be sent:', err.message); // eslint-disable-line no-console
        showEmailFallback(form);
      } finally {
        button.disabled = false;
        button.classList.remove('is-loading');
      }
    });
  });

  // "Get Started" on a pricing card: pick the matching project type in the
  // Hire Me form and note the package, then the link scrolls to the form.
  document.querySelectorAll('[data-package]').forEach((link) => {
    link.addEventListener('click', () => {
      const form = document.getElementById('hireform');
      if (!form) return;
      const radio = form.querySelector(`input[name="project_type"][value="${link.dataset.package}"]`);
      if (radio) {
        radio.checked = true;
        radio.dispatchEvent(new Event('change', { bubbles: true }));
      }
      const pkg = form.querySelector('input[name="package"]');
      const card = link.closest('.price-card');
      if (pkg && card) pkg.value = `${card.querySelector('h3').textContent} (${card.querySelector('.price strong').textContent})`;
    });
  });
})();
