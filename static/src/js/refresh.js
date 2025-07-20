function fetchCurrencyData() {
  fetch('/currency_scraper/data')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const container = document.getElementById('currency-data-container');
      container.innerHTML = ''; 

      data.forEach(item => {
        const row = document.createElement('tr');

        row.innerHTML = `
          <td><img src="/currency_rate/static/img/flags/${item.cFlag}.png" alt="${item.cFlag}" style="width: 32px; height: auto;"></td>
          <td>${item.cName}</td>
          <td>${item.cPrice}</td>
          <td>${item.cDate}</td>
        `;

        container.appendChild(row);
      });
    })
.catch(error => {
  console.error('Error fetching currency data:', error);
  container.innerHTML = '<tr><td colspan="4">⚠️ خطا در دریافت داده</td></tr>';
});
}

document.addEventListener('DOMContentLoaded', () => {
  fetchCurrencyData(); 
  setInterval(fetchCurrencyData, 20 * 1000); 
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
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      document.getElementById('text').classList.add('animate__animated', 'animate__pulse');
      document.getElementById('text3').classList.add('animate__animated', 'animate__pulse');
      document.getElementById('text1').classList.add('animate__animated', 'animate__pulse');
      document.getElementById('text2').classList.add('animate__animated', 'animate__pulse');
      document.getElementById('text3').classList.add('animate__animated', 'animate__pulse');
      document.getElementById('tools').classList.add('animate__animated', 'animate__zoomIn');
      document.getElementById('contact').classList.add('animate__animated', 'animate__zoomIn');
      document.getElementById('icons').classList.add('animate__animated', 'animate__zoomIn');
      document.getElementById('aboutUs').classList.add('animate__fadeIn', 'animate__fast');
      document.getElementById('CPS').classList.add('animate__fadeIn', 'animate__fast');
    } else {
     document.getElementById('text').classList.remove('animate__animated', 'animate__pulse');
      document.getElementById('text1').classList.remove('animate__animated', 'animate__pulse');
      document.getElementById('text2').classList.remove('animate__animated', 'animate__pulse');
      document.getElementById('text3').classList.remove('animate__animated', 'animate__pulse');
      document.getElementById('tools').classList.remove('animate__animated', 'animate__zoomIn');
      document.getElementById('contact').classList.remove('animate__animated', 'animate__zoomIn');
      document.getElementById('icons').classList.remove('animate__animated', 'animate__zoomIn');
      document.getElementById('aboutUs').classList.remove('animate__fadeIn', 'animate__faster');
      document.getElementById('CPS').classList.remove('animate__fadeIn', 'animate__faster');
    }
  });
});

observer.observe(document.getElementById('aboutUs'));

const target = document.getElementById('theTable');
const observer2 = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      target.classList.add('animate__fadeIn', 'animate__fast');

    }
    else{
        target.classList.remove('animate__fadeIn', 'animate__fast');
    }
  });
});

observer2.observe(document.getElementById('theTable'));



});
