
// Data from Django context
const rp_currentDayAvg = {{ current_day_avg }};
const rp_sevenDayAvg = {{ seven_day_avg }};
const rp_thirtyDayAvg = {{ thirty_day_avg }};
const rp_sixMonthAvg = {{ six_month_avg }};
const rp_twelveMonthAvg = {{ twelve_month_avg }};

// Function to determine bar colors based on new conditions
function getColor(value) {
    if (value <= 168) {
        return 'darkgreen'; // Up to 161: DARK GREEN
    } else if (value > 168 && value <= 177) {
        return 'lightgreen'; // 161-170: LIGHT GREEN
    } else if (value > 188 && value <= 200) {
        return 'yellow'; // 170-185: YELLOW
    } else if (value > 200 && value <= 205) {
        return 'orange'; // 185-200: ORANGE
    } else {
        return 'red'; // 200+: RED
    }
}

// Configure chart
const ctx = document.getElementById('invoiceChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Today', '7 Days', '30 Days', '6 Months', '12 Months'],
        datasets: [{
            label: 'Invoice Averages ($)',
            data: [rp_currentDayAvg, rp_sevenDayAvg, rp_thirtyDayAvg, rp_sixMonthAvg, rp_twelveMonthAvg],
            backgroundColor: [
                getColor(rp_currentDayAvg),
                getColor(rp_sevenDayAvg),
                getColor(rp_thirtyDayAvg),
                getColor(rp_sixMonthAvg),
                getColor(rp_twelveMonthAvg)
            ],
            borderColor: ['black', 'black', 'black', 'black', 'black'],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            datalabels: {
                anchor: "end",  // Position above bars
                align: "top",  // Align to the top
                color: "black",  // Label color
                font: {
                    weight: "bold",
                    size: 14
                },
                formatter: function(value) {
                    return `$${value.toFixed(2)}`; // Display as "$xx.xx"
                }
            }
        },
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
