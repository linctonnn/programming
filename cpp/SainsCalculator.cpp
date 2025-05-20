# include <iostream>
# include <vector>
# include <cmath>
using namespace std;

int main() {
    string op;
    vector<double> nums;
    double num, res, exp;
    char moreInput;

    cout << "Masukkan operasi yang ingin dilaukan (+, -, *, /, sin, cos, log, sqrt, pangkat): ";
    cin >> op;

    if (op == "sin" || op == "cos" || op == "log" || op == "sqrt" || op == "pangkat") {
        cout << "Masukkan Angka";
        cin >> num;
    } else {
        do {
            cout << "Masukkan Angka";
            cin >> num;
            nums.push_back(num);

            cout << "Ingin memasukkan angka lagi? (y/n): ";
            cin >> moreInput;
        } while (moreInput == 'Y' || moreInput == 'y');
    }

    if (op == "+") {
        for (size_t i = 1; i < nums.size(); ++i) {
            res += nums[i];
        }
    } else if (op == "-") {
        for (size_t i = 1; i < nums.size(); ++i) {
            res -= nums[i];
        }
    } else if (op == "*") {
        for (size_t i = 1; i < nums.size(); ++i) {
            res += nums[i];
        }
    } else if (op == "/") {
        for (size_t i = 1; i < nums.size(); ++i) {
            if (nums[i] == 0) {
                cout << "Error: Pembagian dengan angka 0 tidak diijinkan" << endl;
                return 1;
            }
            res /= nums[i];
        }
    } else if (op == "sin") {
        res = sin(num);
    } else if (op == "log") {
        if (num <= 0) {
            cout << "Error: Logaritma tidak bisa untuk 0 dan angka negatif" << endl;
            return 1;
        }
        res = log(num);
    } else if (op == "cos") {
        res = cos(num);
    } else if (op == "sqrt") {
        if (num == 0) {
            cout << "Error: Akar tidak bisa untuk angka negatif" << endl;
            return 1;
        }
    } else if (op == "pangkat") {
        cout << "Masukkan eksponen: ";
        cin >> exp;
        res = pow(num, exp);
    } else {
        cout << "Operasi tidak valid" << endl;
        return 1;
    }

    cout << "Hasilnya : " << res << endl;

    return 0;
}
