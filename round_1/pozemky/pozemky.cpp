#include <fstream>
#include <iostream>
#include <string>
using namespace std;

#define MAX_ROWS 20000
#define MAX_OUTPUT 10000

string input_arr[MAX_ROWS];
int outputArr[MAX_OUTPUT];


int populateInputArr(string filePath) {
    // open input file
    fstream inputFile;
    inputFile.open(filePath, ios::in);
    // read input from file into array of strings
    if (inputFile.is_open()) {
        string line;
        int i = 0;
        while(getline(inputFile, line)) {
            if (line != "") {
                input_arr[i] = line;
                i++;
            }
        }
        inputFile.close();
        // return array length
        return i;
    }
}

int populateOutputArr(int inputArrLength)
{
    // loop through input array
    for (int i = 1, l = 0; i < inputArrLength; l++) {
        int animals = stoi(input_arr[i]);
        int task_sum = 0;
        for (int j = 1; j < animals + 1; j++) {

            // split string on spaces
            string row_arr[3];
            string row = input_arr[i+j];
            string delim = " ";
            int k = 0;
            auto start = 0U;
            auto end = row.find(delim);
            while (end != string::npos)
            {
                row_arr[k] = row.substr(start, end - start);
                start = end + delim.length();
                end = row.find(delim, start);
                k++;
            }
            row_arr[k] = row.substr(start, end - start);

            // add current animal land to task_sum
            task_sum += stoi(row_arr[1]) * stoi(row_arr[2]);
        }
        // store task result into the output array
        outputArr[l] = task_sum;
        // set i to the index of new task
        i += animals + 1;
    }
    // return output array length
    return stoi(input_arr[0]);
}

void writeOutputFile(string filePath, int outputArrLength) {
    // open output file
    fstream outputFile;
    outputFile.open("./round_1/pozemky/output.txt", ios::out);
    // write output file
    if (outputFile.is_open()) {
        for (int i = 0; i < outputArrLength; i++) {
            outputFile << outputArr[i] << endl;
        }
    }
    outputFile.close();
}

int main() {
    string inputFile = "./round_1/pozemky/io_example/input.txt";
    string outputFile = "./round_1/pozemky/output";
    int inputArrLength = populateInputArr(inputFile);
    int outputArrLength = populateOutputArr(inputArrLength);
    writeOutputFile(outputFile, outputArrLength);
    return 0;
}