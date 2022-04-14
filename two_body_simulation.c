#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double initial_eccentricity = 0.7;
double initial_q = 0.5;
FILE* data;
typedef struct
{
    double x_pos;
    double y_pos;

}planet;

typedef struct
{
    double state_arr[4];
    planet *cirius;
    planet *tyco;
    double m1;
    double m2;
    double m12;
    double eccentricity; // Eccentricity of the orbit
    double q; // Mass ratio m2 / m1

}twobodymodel;

typedef void (*func)(twobodymodel*);
typedef struct
{
    func show;

}twobodyview;

typedef struct controller{

    twobodymodel* sample;
    twobodyview* show_sample;
    
}controller;

void console(twobodymodel p)
{
    fprintf(data,"x = %lf\t y = %lf\t\t",p.cirius->x_pos,p.cirius->y_pos);
    fprintf(data,"x = %lf\t y = %lf\n",p.tyco->x_pos,p.tyco->y_pos);
}

void console_show_sample(twobodyview* p){
    p->show = (func) console;
}

double initial_velocity(double q, double eccentricity) {
    return sqrt( (1 + q) * (1 + eccentricity) );
}

void reset_state_to_initial_conditions(controller *p) {
    p->sample->q = initial_q;
    p->sample->eccentricity = initial_eccentricity;
    p->sample->state_arr[0]  = 1.0;
    p->sample->state_arr[1]  = 0.0;
    p->sample->state_arr[2]  = 0.0;
    p->sample->state_arr[3]  = initialVelocity(p->sample->q, p->sample->eccentricity);
    p->sample->m1 = 1.0;
    p->sample->m2 = p->sample->q;
    p->sample->m12 = p->sample->m1 + p->sample->m2;
    p->sample->cirius->x_pos =0;
    p->sample->tyco->x_pos =0;
    p->sample->cirius->y_pos =0;
    p->sample->tyco->y_pos =0;
}

double* derivative(controller *p) {
    double *du = malloc(4* sizeof(double));
    double r[2] = {(p->sample->state_arr[0]),(p->sample->state_arr[1])};
    double rr = sqrt(pow(r[0],2) + pow(r[1],2));
    for (int i =0; i<2; i++) {
        du[i] = p->sample->state_arr[i+2];
        du[i+2] = -(1 + p->sample->q) * r[i] / pow(rr,3);
    }
    return du;
}

void runge_kutta_calculate(controller *p,double h) {
    double a[4] = {h/2,h/2,h,0};
    double b[4] = {h/6,h/3,h/3,h/6};
    double u0[4];
    double ut[4];
    double *du;
    for (int i = 0; i < 4; i++) {
        u0[i] = *(p->sample->state_arr + i);
        ut[i] = 0;
    }
    for (int j = 0; j < 4; j++) {
        du = derivative(p);
        for (int i = 0; i < 4; i++) {
            p->sample->state_arr[i] = u0[i] + a[j] * du[i];
            ut[i] = ut[i] + b[j] * du[i];
        }
    }
    for (int i = 0; i < 4; ++i)
        p->sample->state_arr[i] = u0[i] + ut[i];
}

void euler(controller *p,double h){
    double u2[4];
    double *y;
    for (int i = 0; i < 4; i++) {
        u2[i] = *(p->sample->state_arr + i);
    }
    double x[4] = {0.0,0.0,0.0,0.0};
    y = derivative(p);
    for (int i = 0; i < 4; i++) {
        x[i] = u2[i] + h * y[i]; 
    }
    for (int i = 0; i < 4; i++)
    {
        p->sample->state_arr[i] = x[i];
    }       
}

void calculate_new_position(controller *p){
    double r = 1.0;
    double a1 = (p->sample->m2 / p->sample->m12) *r;
    double a2 = (p->sample->m1 / p->sample->m12) *r;
    p->sample->cirius->x_pos = -a2 * p->sample->state_arr[0];
    p->sample->cirius->y_pos = -a2 * p->sample->state_arr[1];
    p->sample->tyco->x_pos = a1 * p->sample->state_arr[0];
    p->sample->tyco->y_pos = a1 * p->sample->state_arr[1];
}
    
void uptade_position(controller *p) {
    double timestep=0.15;
    runge_kutta_calculate(p, timestep);
    calculate_new_position(p);
}

int main()
{
    data = fopen("travelofciriusandtyco.txt", "w");

    planet cirius;
    planet tyco;
    twobodymodel sample;
    twobodyview show_sample;
    controller controller;

    controller.sample = &sample;
    controller.show_sample = &show_sample;
    controller.sample->cirius = &cirius;
    controller.sample->tyco = &tyco;

    console_show_sample(&show_sample);
    reset_state_to_initial_conditions(&controller);

    for (int i = 0; i < 1000; ++i) {
        uptade_position(&controller);
        controller.show_sample->show(controller.sample);
    }

    fclose(data);

    return 0;
}