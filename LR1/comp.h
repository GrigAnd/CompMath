#ifndef COMP_H
#define COMP_H

const int MAX_SIZE = 20;

int gauss(double matrix[MAX_SIZE][MAX_SIZE + 1], int size);
void determinant(double matrix[MAX_SIZE][MAX_SIZE + 1], double &det, int size, int nSwaps);
void revGauss(double matrix[MAX_SIZE][MAX_SIZE + 1], double x[MAX_SIZE], int size);
void vectNevyazok(double matrix[MAX_SIZE][MAX_SIZE + 1], double x[MAX_SIZE], double r[MAX_SIZE], int size);
void printMatrix(double matrix[MAX_SIZE][MAX_SIZE + 1], int size);

#endif
