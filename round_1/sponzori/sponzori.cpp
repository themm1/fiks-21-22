#include <fstream>
#include <iostream>
#include <string>
using namespace std;


#define MAX_ANIMALS 100
#define MAX_SPONSORS 200

struct Sponsor
{
    string name;
    int animals_count;
    int animals[MAX_ANIMALS];
};

struct SponsoredAnimal
{
    int sponsor_id;
    int animal_id;
};

struct SponsoredIndex
{
    int sponsor_id;
    int animal_index;
};

struct SponsorAnimal
{
    string sponsor;
    string animal;
};


class InputHandler
{
    public:
        int animals_count;
        int sponsors_count;
        int input_arr_length;
        string input_file_path;
        string output_file_path;
        string input_arr[MAX_SPONSORS+MAX_ANIMALS+1];
        string *animals;
        Sponsor *sponsors;

        InputHandler(Sponsor sponsors[], string animals[])
        {
            this->animals = animals;
            this->sponsors = sponsors;
        }

    // get input from standard input
    void get()
    {
        cin >> this->animals_count >> this->sponsors_count;
        for (int i = 0; i < this->animals_count; i++)
        {
            int animal_id;
            string animal_name;
            cin >> animal_id >> animal_name;
            this->animals[animal_id] = animal_id;
            this->animals[animal_id] = animal_name;
        }
        cin.ignore();
        for (int i = 0; i < this->sponsors_count; i++)
        {
            string sponsor_line;
            getline(cin, sponsor_line);
            string sponsor_arr[MAX_ANIMALS+2];
            split(sponsor_line, sponsor_arr);

            Sponsor sponsor;
            sponsor.name = sponsor_arr[0];
            sponsor.animals_count = stoi(sponsor_arr[1]);
            for (int j = 0; j < sponsor.animals_count; j++)
            {
                sponsor.animals[j] = stoi(sponsor_arr[j+2]);
            }
            this->sponsors[i] = sponsor;
        }
    }

    // method used to run program using text file as input
    void loadRead(string input_file_path)
    {
        this->input_file_path = input_file_path;
        this->readFile();
        string counts[2];
        split(this->input_arr[0], counts);
        this->animals_count = stoi(counts[0]);
        this->sponsors_count = stoi(counts[1]);
        
        for (int i = 1; i < this->animals_count+1; i++)
        {
            string current_animal[2];
            split(this->input_arr[i], current_animal);
            this->animals[stoi(current_animal[0])] = current_animal[1];
        }

        for (int i = animals_count+1; i < this->input_arr_length; i++)
        {
            string current_sponsor_arr[animals_count];
            split(this->input_arr[i], current_sponsor_arr);
            Sponsor current_sponsor;

            current_sponsor.name = current_sponsor_arr[0];
            current_sponsor.animals_count = stoi(current_sponsor_arr[1]);
            for (int j = 2; j < current_sponsor.animals_count+2; j++) {
                current_sponsor.animals[j-2] = stoi(current_sponsor_arr[j]);
            }
            this->sponsors[i-animals_count-1] = current_sponsor;
        }
    }
    
    void readFile()
    {
        fstream inputFile;
        inputFile.open(this->input_file_path, ios::in);
        if (inputFile.is_open())
        {
            string line;
            int i = 0;
            while(getline(inputFile, line))
            {
                if (line != "") {
                    this->input_arr[i] = line;
                    i++;
                }
            }
            inputFile.close();
            this->input_arr_length = i;
        }
    }

    static int split(string str, string str_arr[])
    {
        string delim = " ";
        int i = 0;
        auto start = 0U;
        auto end = str.find(delim);
        while (end != string::npos)
        {
            str_arr[i] = str.substr(start, end - start);
            start = end + delim.length();
            end = str.find(delim, start);
            i++;
        }
        str_arr[i] = str.substr(start, end - start);
        return i + 1;
    }
};

class FindBestCombination
{
    public:
        int animals_count;
        int sponsors_count;
        int best_comb_length = 0;
        SponsoredAnimal best_combination[MAX_ANIMALS];
        SponsoredIndex sponsors_indices[MAX_SPONSORS];
        Sponsor *sponsors;
        
        FindBestCombination(Sponsor sponsors[], int animals_count, int sponsors_count)
        {
            this->sponsors = sponsors;
            this->sponsors_count = sponsors_count;
            this->animals_count = animals_count;
            // create indices array which will represent current combination
            for (int i = 0; i < sponsors_count; i++)
            {
                SponsoredIndex sponsored_animal;
                sponsored_animal.sponsor_id = i;
                sponsored_animal.animal_index = 0;
                this->sponsors_indices[i] = sponsored_animal;
            }
        }

    void updateBest()
    {
        SponsoredAnimal current_comb[MAX_SPONSORS];
        int hash[MAX_SPONSORS] = {0};
        int sponsored_animals_count = 0;
        // mark sponsors with duplicate animals from current combination
        // and translate animal indices to their ids
        for (int i = 0; i < this->sponsors_count; i++)
        {
            int current_animal_id = sponsors[i].animals[sponsors_indices[i].animal_index];
            int current_sponsor_id = sponsors[i].animals[sponsors_indices[i].sponsor_id];
            if (hash[current_animal_id] == 0)
            {
                hash[current_animal_id] = 1;
                current_comb[i].animal_id = current_animal_id;
                current_comb[i].sponsor_id = current_sponsor_id;
                sponsored_animals_count++;
            }
            else
            {
                // mark sponsor with already sponsored animal
                current_comb[i].animal_id = -1;
                current_comb[i].sponsor_id = -1;
            }
        }
        // copy current combination to best combination if is better
        if (sponsored_animals_count > this->best_comb_length)
        {
            this->best_comb_length = sponsored_animals_count;
            for (int i = 0; i < this->sponsors_count; i++)
            {
                this->best_combination[i].animal_id = current_comb[i].animal_id;
                this->best_combination[i].sponsor_id = current_comb[i].sponsor_id;
            }
        }
    }

    void findBest()
    {
        // loop until no other combinations are possible
        while (true)
        {
            bool all_combinations_done = true;
            this->updateBest();
            // find array which index from indices array could be incremented
            for (int i = this->sponsors_count-1; i >= 0; i--)
            {
                if (this->sponsors_indices[i].animal_index + 1 < sponsors[i].animals_count)
                {
                    all_combinations_done = false;
                    this->sponsors_indices[i].animal_index += 1;
                    // set indices of all arrays that are on right side to the current array to 0
                    for (int j = i+1; j < this->sponsors_count; j++)
                    {
                        this->sponsors_indices[j].animal_index = 0;
                    }
                    // return if no better combination can be found
                    if (this->best_comb_length == this->sponsors_count ||
                        this->best_comb_length == this->animals_count)
                    {
                        return;
                    }
                    break;
                }
            }
            if (all_combinations_done)
            {
                return;
            }
        }
    }
};


class Result
{
    public:
        int sponsors_count;
        int result_length;
        SponsorAnimal result[MAX_ANIMALS];
        string *animals;
        Sponsor *sponsors;
        SponsoredAnimal *best_combination;
        
        Result(Sponsor sponsors[], string animals[],
            SponsoredAnimal best_combination[], int sponsors_count)
        {
            this->sponsors = sponsors;
            this->animals = animals;
            this->best_combination = best_combination;
            this->sponsors_count = sponsors_count;
            this->populate();
        }

    void populate()
    {
        int j = 0;
        for (int i = 0; i < this->sponsors_count; i++)
        {
            // add sponsor-animal pair to result if has unique animal
            if (this->best_combination[i].animal_id >= 0)
            {
                this->result[j].sponsor = this->sponsors[i].name;
                this->result[j].animal = this->animals[this->best_combination[i].animal_id];
                j++;
            }
        }
        this->result_length = j;
    }

    void merge(int left, int mid, int right)
    {
        // copy left part of an array to separate array
        int left_len = mid - left + 1;
        SponsorAnimal left_part[left_len];
        for (int i = 0; i < left_len; i++)
        {
            left_part[i] = this->result[left+i];
        }
        
        // copy right part of an array to separate array
        int right_len = right - mid;
        SponsorAnimal right_part[right_len];
        for (int i = 0; i < right_len; i++)
        {
            right_part[i] = this->result[i+mid+1];
        }

        // merge subarrays into main array
        int left_index = 0, right_index = 0, merged_index = left;
        for (;left_index < left_len && right_index < right_len; merged_index++)
        {
            // loop through words characters until one character differs
            for (int i = 0;; i++)
            {
                if (i >= right_part[right_index].animal.length() || 
                    left_part[left_index].animal[i] > right_part[right_index].animal[i])
                {
                    this->result[merged_index] = right_part[right_index];
                    right_index++;
                    break;
                }
                else if (i >= left_part[left_index].animal.length() ||
                    left_part[left_index].animal[i] < right_part[right_index].animal[i])
                {
                    this->result[merged_index] = left_part[left_index];
                    left_index++;
                    break;
                }
            }
        }

        // add remaining elements to array
        for (;left_index < left_len; left_index++, merged_index++)
        {
            this->result[merged_index] = left_part[left_index];
        }
        for (;right_index < right_len; right_index++, merged_index++)
        {
            this->result[merged_index] = right_part[right_index];
        }
    }

    void sort(int left, int right)
    {
        if (left >= right)
        {
            return;
        }
        int mid = left + (right - left) / 2;
        // recursively sort array by splitting it into halves
        sort(left, mid);
        sort(mid+1, right);
        merge(left, mid, right);
    }

    void print()
    {
        for (int i = 0; i < this->result_length; i++)
        {
            cout << this->result[i].animal << " " << this->result[i].sponsor << endl;
        }
    }
};


int main()
{
    Sponsor sponsors[MAX_SPONSORS];
    string animals[MAX_ANIMALS];
    SponsoredAnimal best_combination[MAX_SPONSORS];

    InputHandler input(sponsors, animals);
    input.get();
    // input.loadRead("path to input file");

    FindBestCombination combinations(sponsors, input.animals_count, input.sponsors_count);
    combinations.findBest();

    if (combinations.best_comb_length == input.animals_count)
    {
        cout << "Ano" << endl;
    }
    else 
    {
        cout << "Ne" << endl;
    }
    Result result(sponsors, animals, combinations.best_combination, input.sponsors_count);
    result.sort(0, combinations.best_comb_length-1);
    result.print();
}