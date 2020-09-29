$(document).ready(function(){
$("#demo").awesomeCloud({
"size" : {
"<a href='https://www.jqueryscript.net/tags.php?/grid/'>grid</a>" : 1, // word spacing, smaller is more tightly packed
"factor" : 0, // font resize factor, 0 means automatic
"normalize" : false // reduces outliers for more attractive output
},
"color" : {
"background" : "rgba(255,255,255,0)", // background color, transparent by default
"start" : "#20f", // color of the smallest font, if options.color = "gradient""
"end" : "rgb(200,0,0)" // color of the largest font, if options.color = "gradient"
},
"options" : {
"color" : "random-dark", // random-light, random-dark, gradient
"rotationRatio" : 0.35, // 0 is all horizontal, 1 is all vertical
"printMultiplier" : 3, // set to 3 for nice printer output; higher numbers take longer
"sort" : "random" // highest, lowest or random
},
"font" : "'Times New Roman', Times, serif", //  the CSS font-family string
"shape" : "square" // circle, square, star or a theta function describing a shape
});
});