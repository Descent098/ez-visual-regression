/* globals Chart:false, feather:false */

(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July'
      ],
      datasets: [{
        label: 'My First Dataset',
        data: [75, 80, 80, 81, 15, 85, 40], // New
        backgroundColor: [
          'rgba(111, 99, 132, 0.2)',
          'rgba(255, 222, 64, 0.2)',
          'rgba(255, 205, 121, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
          'rgb(111, 99, 132)',
          'rgb(255, 222, 64)',
          'rgb(255, 205, 121)',
          'rgb(75, 192, 192)',
          'rgb(54, 162, 235)',
          'rgb(153, 102, 255)',
          'rgb(201, 203, 207)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          min: 0, // minimum value
          max: 100 // maximum value
        }
      }
    },
    animation: false
  })
})()
