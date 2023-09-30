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
        label: 'Based',
        data: [657, 480, 680, 381, 225, 30, 400], // Old
        // data: [65, 80, 80, 81, 25, 85, 40], // New
        backgroundColor: [
          'rgba(0, 0, 0, 0.9)',
          'rgba(0, 0, 0, 0.9)',
          'rgba(0, 0, 0, 0.9)',
          'rgba(0, 0, 0, 0.9)',
          'rgba(0, 0, 0, 0.9)',
          'rgba(0, 0, 0, 0.9)',
          'rgba(0, 0, 0, 0.9)'
        ],
        borderColor: [
          'rgb(0, 0, 0)',
          'rgb(0, 0, 0)',
          'rgb(0, 0, 0)',
          'rgb(0, 0, 0)',
          'rgb(0, 0, 0)',
          'rgb(0, 0, 0)',
          'rgb(0, 0, 0)',
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
