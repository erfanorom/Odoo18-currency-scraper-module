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
});
