uniform vec2 pos;


const float PARTICLE_COUNT = 100.0;

const float MAX_PARTICLE_DISTANCE = 0.3;

const float PARTICLE_SIZE = 0.004;
const float BURST_TIME = 2.0;
const float DEFAULT_BRIGHTNESS = 0.0005;
const float TWINKLE_SPEED = 10.0;
const float TWOPI = 6.2832;

vec2 Hash12_Polar(float t){
    float angle = fract(sin(t * 674.3) * 453.2) * TWOPI;
    float distance = fract(sin((t + angle) * 724.3) * 341.2);
    return vec2(sin(angle), cos(angle)) * distance;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 npos = (pos - .5 * iResolution.xy) / iResolution.y;
    vec2 uv = (fragCoord - .5 * iResolution.xy) / iResolution.y;

    uv -= npos;

    float alpha = 0.0;
    float timeFract = fract(iTime * 1 / BURST_TIME);
    float particletime = iTime;
    float brightness = 0.0;
    

    for (float i= 0.; i < PARTICLE_COUNT; i++){
        float seed = i + 1.0;
        vec2 dir = Hash12_Polar(seed);
        vec2 particlePosition = dir * MAX_PARTICLE_DISTANCE * particletime;
        float d = length(uv - particlePosition);
        brightness =  1.0 + DEFAULT_BRIGHTNESS * (sin(particletime * TWINKLE_SPEED + i) * .5 + .5);
        alpha += DEFAULT_BRIGHTNESS / d;
        
    }


    fragColor = vec4(brightness, brightness, brightness, alpha * (1.0 - particletime));
    
}