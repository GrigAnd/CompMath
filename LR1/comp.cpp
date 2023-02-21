#include "comp.h"

#include <iostream>
using namespace std;
#include <iomanip>

void printMatrix(double matrix[MAX_SIZE][MAX_SIZE + 1], int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            cout << setw(15) << matrix[i][j] << " ";
        }
        cout << "| " << setw(15) << matrix[i][size];
        cout << endl;
    }
    cout << endl;
}

int gauss(double matrix[MAX_SIZE][MAX_SIZE + 1], int size) {
    int nSwaps = 0;
    for (int i = 0; i < size - 1; i++) {
        if (matrix[i][i] == 0) {
            // Поиск ненулевого элемента в столбце i и перестановка строк
            int j = i + 1;
            while (j < size && matrix[j][i] == 0) {
                j++;
            }
            if (j == size) {
                // Матрица вырождена
                return -1;
            }
            for (int k = i; k <= size; k++) {
                double temp = matrix[i][k];
                matrix[i][k] = matrix[j][k];
                matrix[j][k] = temp;
            }
            nSwaps++;
            cout << "Перестановка строк " << i + 1 << " и " << j + 1 << endl;
            printMatrix(matrix, size);
        }
        for (int j = i + 1; j < size; j++) {
            float factor = matrix[j][i] / matrix[i][i];
            for (int k = i; k <= size; k++) {
                matrix[j][k] -= (float)(factor * matrix[i][k]);
            }
        }
        
        cout << "Строка " << i + 2 << " приведена к треугольному виду" << endl;
        printMatrix(matrix, size);
    }

    for (int i = 0; i < size; i++) {
        for (int j = 0; j < i; j++) {
            matrix[i][j] = 0;
        }
    }

    return nSwaps;
}

void determinant(double matrix[MAX_SIZE][MAX_SIZE + 1], double &det, int size, int nSwaps) {
    det = nSwaps % 2 == 0 ? 1 : -1;
    for (int i = 0; i < size; i++) {
        det *= matrix[i][i];
    }
}

void revGauss(double matrix[MAX_SIZE][MAX_SIZE + 1], double x[MAX_SIZE], int size) {
    for (int i = size - 1; i >= 0; i--) {
        x[i] = matrix[i][size];
        for (int j = i + 1; j < size; j++) {
            x[i] -= matrix[i][j] * (float)x[j];
        }
        x[i] /= matrix[i][i];
    }
}

void vectNevyazok(double matrix[MAX_SIZE][MAX_SIZE + 1], double x[MAX_SIZE], double r[MAX_SIZE], int size) {
    for (int i = 0; i < size; i++) {
        // r[i] = 0;
        double nev = 0.0;
        for (int j = 0; j < size; j++) {
            nev += matrix[i][j] * x[j];
        }
        nev -= matrix[i][size];
        r[i] = nev;
    }
}