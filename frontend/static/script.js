const filepath = "{{ filepath }}";
console.log("Filepath:", filepath);

function updateChart(selectEl) {
  const x_col = selectEl.value;
  const y_col = selectEl.getAttribute('data-ycol');

  fetch('/update_column_chart', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ x_col, y_col, filepath })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) return;
    const ts = new Date().getTime();
    document.getElementById('line-' + y_col).src = data.line + '?t=' + ts;
    document.getElementById('bar-'  + y_col).src = data.bar  + '?t=' + ts;
  })
  .catch(err => console.error('Error:', err));
}