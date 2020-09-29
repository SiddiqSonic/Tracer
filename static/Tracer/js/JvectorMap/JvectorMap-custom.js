

var gdpData = {
  "AF": 16.63,
  "AL": 11.58,
  "DZ": 158.97,
};


$('#world-map-gdp').vectorMap({
  map: 'world_mill',
  series: {
    regions: [{
      values: gdpData,
      scale: ['#C8EEFF', '#0071A4'],
      normalizeFunction: 'polynomial'
    }]
  },
  onRegionTipShow: function(e, el, code){
    el.html(el.html()+' (GDP - '+gdpData[code]+')');
  }
});