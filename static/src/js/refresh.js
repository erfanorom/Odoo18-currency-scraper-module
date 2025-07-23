function fetchCurrencyData() {
  const container = document.getElementById('currency-data-container');
  const updateTime = document.getElementById('update-time');
  const errorDiv = document.getElementById('js-error');

  fetch('/currency_scraper/data')
    .then(response => {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(data => {
      container.innerHTML = ''; 
      let i = 1;
      data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${i}</td>
          <td><img src="/currency_rate/static/img/flags/${item.cFlag}.png" alt="${item.cFlag}" style="width: 32px; height: auto;"></td>
          <td>${item.cName}</td>
          <td>${item.cPrice} ریال</td>
        `;
        container.appendChild(row);
        i++;
      });

      if (data.length > 0) {
        updateTime.textContent = `آخرین بروزرسانی: ${data[0].cDate}`;
      } else {
        updateTime.textContent = 'دیتایی دریافت نشد';
      }

      errorDiv.classList.add('d-none');
    })
    .catch(error => {
      console.error('Error fetching currency data:', error);
      container.innerHTML = '<tr><td class="text-center" colspan="5">⚠️ خطا در دریافت داده</td></tr>';
      updateTime.textContent = '--:--:--';
      errorDiv.classList.remove('d-none');
    });
}

window.addEventListener('load', () => {
  fetchCurrencyData(); 
  setInterval(fetchCurrencyData, 20000);
});

document.addEventListener('DOMContentLoaded', () => {

  var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink', 'rounded')
        } else {
            navbarCollapsible.classList.add('navbar-shrink', 'rounded')
        }

    };
    navbarShrink();
    document.addEventListener('scroll', navbarShrink);
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });
    const loader = document.getElementById('page-loader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
        }, 300);
    }
const animations = [
    { id: 'text', classes: ['animate__animated', 'animate__pulse'] },
    { id: 'text1', classes: ['animate__animated', 'animate__pulse'] },
    { id: 'text2', classes: ['animate__animated', 'animate__pulse'] },
    { id: 'text3', classes: ['animate__animated', 'animate__pulse'] },
    { id: 'tools', classes: ['animate__animated', 'animate__zoomIn'] },
    { id: 'contact', classes: ['animate__animated', 'animate__zoomIn'] },
    { id: 'icons', classes: ['animate__animated', 'animate__zoomIn'] },
    { id: 'aboutUs', classes: ['animate__fadeIn', 'animate__fast'] },
    { id: 'CPS', classes: ['animate__fadeIn', 'animate__faster'] }
  ];

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      animations.forEach(({ id, classes }) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (entry.isIntersecting) {
          el.classList.add(...classes);
        } else {
          el.classList.remove(...classes);
        }
      });
    });
  });

observer.observe(document.getElementById('aboutUs'));

const tableAnimation = {
  id: 'theTable',
  classes: ['animate__fadeIn', 'animate__fast']
};

const target = document.getElementById(tableAnimation.id);

const observer2 = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!target) return;

    if (entry.isIntersecting) {
      target.classList.add(...tableAnimation.classes);
    } else {
      target.classList.remove(...tableAnimation.classes);
    }
  });
});

observer2.observe(target);



});