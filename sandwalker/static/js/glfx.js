// This is based on https://github.com/paulirish/webgl-boilerplate.

window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;

var canvas;
var gl;
var buffer;
var vertex_shader;
var fragment_shader;
var currentProgram;
var vertex_position;
var timeLocation;
var resolutionLocation;
var scaleFactor;
var rndSeed;

var parameters = {
    start_time: new Date().getTime(), 
    time: 0, 
    screenWidth: 0, 
    screenHeight: 0,
    scaleFactor: Math.random() * 0.5 + 0.2,
    rndSeed: Math.random()
};
 
function init() {
    glfx_vertex = document.getElementById('glfx-vertex');
    glfx_fragment = document.getElementById('glfx-fragment');
    if (!glfx_vertex || !glfx_fragment) {
	return;
    }

    vertex_shader = glfx_vertex.textContent;
    fragment_shader = glfx_fragment.textContent;
 
    canvas = document.querySelector('#glfx');
 
    // Initialise WebGL.
    gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
    if (!gl) {
	console.log("Unable to initialize WebGL");
	return;
    }
 
    // Create Vertex buffer (2 triangles).
    buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0]), gl.STATIC_DRAW);
 
    currentProgram = createProgram(vertex_shader, fragment_shader);
    timeLocation = gl.getUniformLocation(currentProgram, 'time');
    scaleFactor = gl.getUniformLocation(currentProgram, 'scaleFactor');
    rndSeed = gl.getUniformLocation(currentProgram, 'rndSeed');
    resolutionLocation = gl.getUniformLocation(currentProgram, 'resolution');
}
 
function createProgram(vertex, fragment) { 
    var program = gl.createProgram();
    var vs = createShader(vertex, gl.VERTEX_SHADER);
    var fs = createShader(fragment, gl.FRAGMENT_SHADER);

    if (vs == null || fs == null) {
	console.log("Unable to create shaders");
	return;
    }
 
    gl.attachShader(program, vs);
    gl.attachShader(program, fs);
    gl.deleteShader(vs);
    gl.deleteShader(fs);
 
    gl.linkProgram(program);
 
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
	console.log("Unable to load shader, status=" + gl.getProgramParameter(program, gl.VALIDATE_STATUS));
	console.log("Unable to load shader, error=" + gl.getError());
	return;
    }
    
    return program;
}
 
function createShader(src, type) {
    var shader = gl.createShader(type);
 
    gl.shaderSource(shader, src);
    gl.compileShader(shader);
 
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
	console.log("Unable to compile shader: " + gl.getShaderInfoLog(shader));
	return null;
    }

    return shader;
}

function resize() {
    if (!canvas) {
	return;
    }

    if (canvas.width != canvas.clientWidth || canvas.height != canvas.clientHeight) {	
	canvas.width = canvas.clientWidth;
	canvas.height = canvas.clientHeight;

	parameters.screenWidth = canvas.width;
	parameters.screenHeight = canvas.height;

	gl.viewport(0, 0, canvas.width, canvas.height);
    }
}
 
function animate() { 
    resize();
    render();
    requestAnimationFrame(animate);
}

function render() {
    if (!currentProgram) {
	return;
    }
 
    parameters.time = new Date().getTime() - parameters.start_time;
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
 
    // Load program into GPU
    gl.useProgram(currentProgram);
 
    // Set values to program variables
    gl.uniform1f(timeLocation, parameters.time / 1000);
    gl.uniform1f(scaleFactor, parameters.scaleFactor)
    gl.uniform1f(rndSeed, parameters.rndSeed)
    gl.uniform2f(resolutionLocation, parameters.screenWidth, parameters.screenHeight);
 
    // Render geometry
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.vertexAttribPointer(vertex_position, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vertex_position);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
    gl.disableVertexAttribArray(vertex_position);
}

init();
animate();
