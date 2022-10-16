//pulls center pos from explosion class
uniform vec2 pos;

// sets constants required for the render of the explosion 
const float PARTICLE_COUNT = 100.0;

const float MAX_PARTICLE_DISTANCE = 0.3;

const float PARTICLE_SIZE = 0.004;
//BURST_TIME is how long it takes to cycle render
const float BURST_TIME = 2.0;
const float DEFAULT_BRIGHTNESS = 0.0005;
const float TWINKLE_SPEED = 10.0;
const float TWOPI = 6.2832;

//this runs to determine a location for each particle in the explosion
//done in polar coords to make the explosion look more circular
vec2 Hash12_Polar(float t){
    float angle = fract(sin(t * 674.3) * 453.2) * TWOPI;
    float distance = fract(sin((t + angle) * 724.3) * 341.2);
    return vec2(sin(angle), cos(angle)) * distance;
}

//main shader program
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    //sets up window and sets up coordinate system for shader
    vec2 npos = (pos - .5 * iResolution.xy) / iResolution.y;
    vec2 uv = (fragCoord - .5 * iResolution.xy) / iResolution.y;

    uv -= npos;

    float alpha = 0.0;
    float particletime = iTime;
    float brightness = 0.0;
    
    //sets up each particle and amount of particle runs is determined by PARTICLE_COUNT
    for (float i= 0.; i < PARTICLE_COUNT; i++){
        float seed = i + 1.0;
        //sets particle pos
        vec2 dir = Hash12_Polar(seed);
        //updates particle pos which moves from origin over time
        vec2 particlePosition = dir * MAX_PARTICLE_DISTANCE * particletime;
        float d = length(uv - particlePosition);
        //particle will lose brightness as it moves from point of origin and will also twinkle
        brightness =  1.0 + DEFAULT_BRIGHTNESS * (sin(particletime * TWINKLE_SPEED + i) * .5 + .5);
        alpha += DEFAULT_BRIGHTNESS / d;
        
    }

    //send particle parameters to render to update pixel info on screen
    fragColor = vec4(brightness, brightness, brightness, alpha * (1.0 - particletime));
    
}