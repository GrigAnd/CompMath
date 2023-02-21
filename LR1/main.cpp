#include <fstream>
#include <iomanip>
#include <iostream>

#include "comp.h"

using namespace std;


void printVector(double vector[MAX_SIZE], int size, string name) {
    cout << name << " = (";
    for (int i = 0; i < size; i++) {
        cout << vector[i];
        if (i != size - 1) {
            cout << ", ";
        }
    }
    cout << ")" << endl;
}

void inputSize(int &size) {
    string strSize;
    bool isValidSize = false;
    while (!isValidSize) {
        cout << "Введите размерность матрицы: ";
        cin >> strSize;
        isValidSize = true;
        for (int i = 0; i < strSize.length(); i++) {
            if (!isdigit(strSize[i])) {
                cout << "Ошибка: размерность должна быть целым числом" << endl;
                isValidSize = false;
                break;
            }
        }
        if (!isValidSize) {
            continue;
        }
        size = stoi(strSize);
        if (size < 1 || size > MAX_SIZE) {
            cout << "Ошибка: размерность должна быть в диапазоне [1, " << MAX_SIZE << "]" << endl;
            isValidSize = false;
        }
    }
    cout << endl;
}

void inputMatrix(double matrix[MAX_SIZE][MAX_SIZE + 1], int size) {
    for (int i = 0; i < size; i++) {
        cout << "Введите элементы " << i + 1 << " строки (разделенные пробелом): ";
        bool isValidRow = true;
        for (int j = 0; j <= size; j++) {
            string strElement;
            cin >> strElement;
            if (strElement.find(',') != string::npos) {
                strElement.replace(strElement.find(','), 1, ".");
            }
            for (int k = 0; k < strElement.length(); k++) {
                if (!isdigit(strElement[k]) && strElement[k] != '.' && strElement[k] != '-') {
                    cout << "Ошибка: элемент[" << i << "][" << j << "] должен быть числом" << endl;
                    isValidRow = false;
                    cin.ignore(1000, '\n');
                    break;
                }
            }

            if (!isValidRow) {
                break;
            }

            matrix[i][j] = stod(strElement);
        }
        if (!isValidRow) {
            cout << "Повторите ввод " << i + 1 << " строки" << endl;
            i--;
        }
    }
    cout << endl;
}

bool inputFromFile(double matrix[MAX_SIZE][MAX_SIZE + 1], int &size, string fileName) {
    ifstream file(fileName);
    if (!file.is_open()) {
        cout << "Ошибка: файл " << fileName << " не найден" << endl;
        return false;
    }

    string strSize;
    getline(file, strSize);
    size = stoi(strSize);
    if (size < 1 || size > MAX_SIZE) {
        cout << "Ошибка: размерность должна быть в диапазоне [1, " << MAX_SIZE << "]" << endl;
        return false;
    }

    for (int i = 0; i < size; i++) {
        string strRow;
        getline(file, strRow);
        if (strRow.empty()) {
            cout << "Ошибка: строка " << i + 1 << " пуста" << endl;
            return false;
        }

        int pos = 0;
        for (int j = 0; j <= size; j++) {
            string strElement;
            pos = strRow.find(' ');
            if (pos == string::npos) {
                strElement = strRow;
            } else {
                strElement = strRow.substr(0, pos);
                strRow.erase(0, pos + 1);
            }

            if (strElement.find(',') != string::npos) {
                strElement.replace(strElement.find(','), 1, ".");
            }
            for (int k = 0; k < strElement.length(); k++) {
                if (!isdigit(strElement[k]) && strElement[k] != '.' && strElement[k] != '-') {
                    cout << "Ошибка: элемент[" << i << "][" << j << "] должен быть числом" << endl;
                    return false;
                }
            }

            matrix[i][j] = stod(strElement);
        }
    }

    return true;
}

int main(int argc, char *argv[]) {
    double matrix[MAX_SIZE][MAX_SIZE + 1];
    int size;

    if (argc > 1) {
        if (!inputFromFile(matrix, size, argv[1])) {
            return 1;
        }
    } else {
        inputSize(size);
        inputMatrix(matrix, size);
    }

    cout << "Введённая матрица:" << endl;
    printMatrix(matrix, size);

    // Прямой ход метода Гаусса
    int nSwaps = gauss(matrix, size);
    cout << "Количество перестановок строк: " << nSwaps << endl << endl;
    if (nSwaps == -1) {
        cout << "Ошибка: матрица вырождена" << endl;
        return 1;
    }

    // Вычисление определителя
    double det = 1.0;
    determinant(matrix, det, size, nSwaps);

    // Обратный ход метода Гаусса
    double x[MAX_SIZE];
    revGauss(matrix, x, size);

    // Вычисление вектора невязок
    double r[MAX_SIZE];
    vectNevyazok(matrix, x, r, size);

    cout << "Треугольная матрица:" << endl;
    printMatrix(matrix, size);
    cout << "Определитель = " << det << endl
         << endl;

    cout << "Вектор неизвестных:" << endl;
    printVector(x, size, "x");

    cout << "Вектор невязок:" << endl;
    printVector(r, size, "r");

    return 0;
}