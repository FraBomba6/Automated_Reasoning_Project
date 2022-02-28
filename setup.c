#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "string.h"
#include "sys/stat.h"

typedef struct{
    int x;
    int y;
    int s;
} cell;

cell *gen_cells(int n, int blocked, int occupied, int hearts, int clubs, int spades, int diamonds) {
    int x, y, hearts_counter=0, clubs_counter=0, spades_counter=0, diamonds_counter=0;
    cell *cells = malloc(blocked + occupied);
    for (int b = blocked; b > 0; b--) {
        int present;
        do {
            present = 0;
            x = (rand() % n) + 1;
            y = (rand() % n) + 1;
            for(int l = 0; l < blocked-b; l++) {
                if (cells[l].x == x && cells[l].y == y)
                    present = 1;
            }
        } while (present == 1);
        cell c = {x, y, 5};
        cells[blocked - b] = c;
    }
    for (int o = occupied; o > 0; o--) {
        int present, balanced, s;
        do {
            present = 0;
            x = (rand() % n) + 1;
            y = (rand() % n) + 1;
            for(int l = 0; l < blocked + occupied - o; l++) {
                if (cells[l].x == x && cells[l].y == y)
                    present = 1;
            }
        } while (present == 1);
        do {
            balanced = 1;
            s = (rand() % 4) + 1;
            switch (s) {
                case 1:
                    if (hearts_counter + 1 > hearts)
                        balanced = 0;
                    else
                        hearts_counter += 1;
                    break;
                case 2:
                    if (clubs_counter + 1 > clubs)
                        balanced = 0;
                    else
                        clubs_counter += 1;
                    break;
                case 3:
                    if (spades_counter + 1 > spades)
                        balanced = 0;
                    else
                        spades_counter += 1;
                case 4:
                    if (diamonds_counter + 1 > diamonds)
                        balanced = 0;
                    else
                        diamonds_counter += 1;
            }
        } while (balanced == 0);
        cell c = {x, y, s};
        cells[blocked + occupied - o] = c;
    }
    return cells;
}

void print_matrix(int n, int blocked, int occupied, cell *cells) {
    for (int x = 0; x < n; x++) {
        printf("\t\t");
        for (int y = 0; y < n; y++) {
            int present = 0;
            for (int l = 0; l < blocked + occupied; l++) {
                if (cells[l].x-1 == x && cells[l].y-1 == y) {
                    printf("| %d ", cells[l].s);
                    present = 1;
                }
            }
            if (present == 0)
                printf("| _ ");
        }
        printf("|\n");
    }
}

void gen_dzn(int n, int hearts, int clubs, int spades, int diamonds, cell *cells, int cells_l, char *mzn_dir, int m) {
    char file_name[15] = "";
    char file_number[4] = "";
    char file_path[50] = "";
    sprintf(file_number, "%02d", m);
    strcat(file_name, "/");
    strcat(file_name, file_number);
    strcat(file_name, "_data");
    strcat(file_name, ".dzn");
    strcat(file_path, mzn_dir);
    strcat(file_path, file_name);

    FILE *fptr;
    fptr = fopen(file_path, "w");
    fprintf(fptr, "%s", "n=");
    fprintf(fptr, "%d", n);
    fprintf(fptr, "%s", ";\n");
    fprintf(fptr, "%s", "hearts=");
    fprintf(fptr, "%d", hearts);
    fprintf(fptr, "%s", ";\n");
    fprintf(fptr, "%s", "clubs=");
    fprintf(fptr, "%d", clubs);
    fprintf(fptr, "%s", ";\n");
    fprintf(fptr, "%s", "spades=");
    fprintf(fptr, "%d", spades);
    fprintf(fptr, "%s", ";\n");
    fprintf(fptr, "%s", "diamonds=");
    fprintf(fptr, "%d", diamonds);
    fprintf(fptr, "%s", ";\n");
    fprintf(fptr, "%s", "m=array2d(1..n, 1..n,[\n");
    for (int x = 0; x < n; x++) {
        fprintf(fptr, "%s", "\t");
        for (int y = 0; y < n; y++) {
            int present = 0;
            for (int l = 0; l < cells_l; l++) {
                if (cells[l].x-1 == x && cells[l].y-1 == y) {
                    fprintf(fptr, "%d", cells[l].s);
                    present = 1;
                }
            }
            if (present == 0)
                fprintf(fptr, "%s", "_");
            if ((x < n-1 && y < n-1) || (x < n-1 && y == n-1) || (x == n-1 && y < n-1))
                fprintf(fptr, "%s", ",");
        }
        fprintf(fptr, "%s", "\n");
    }
    fprintf(fptr, "%s", "]);\n");
    fclose(fptr);
}

void gen_lp(int n, int hearts, int clubs, int spades, int diamonds, cell *cells, int cells_l, char *asp_dir, int m) {
    char file_name[15] = "";
    char file_number[4] = "";
    char file_path[50] = "";
    sprintf(file_number, "%02d", m);
    strcat(file_name, "/");
    strcat(file_name, file_number);
    strcat(file_name, "_data");
    strcat(file_name, ".lp");
    strcat(file_path, asp_dir);
    strcat(file_path, file_name);

    FILE *fptr;
    fptr = fopen(file_path, "w");
    fprintf(fptr, "%s", "#const n=");
    fprintf(fptr, "%d", n);
    fprintf(fptr, "%s", ".\n");
    fprintf(fptr, "%s", "#const hearts=");
    fprintf(fptr, "%d", hearts);
    fprintf(fptr, "%s", ".\n");
    fprintf(fptr, "%s", "#const clubs=");
    fprintf(fptr, "%d", clubs);
    fprintf(fptr, "%s", ".\n");
    fprintf(fptr, "%s", "#const spades=");
    fprintf(fptr, "%d", spades);
    fprintf(fptr, "%s", ".\n");
    fprintf(fptr, "%s", "#const diamonds=");
    fprintf(fptr, "%d", diamonds);
    fprintf(fptr, "%s", ".\n");
    for (int l = 0; l < cells_l; l++) {
        fprintf(fptr, "%s", "griglia(");
        fprintf(fptr, "%d", cells[l].x);
        fprintf(fptr, "%s", ",");
        fprintf(fptr, "%d", cells[l].y);
        fprintf(fptr, "%s", ",");
        fprintf(fptr, "%d", cells[l].s);
        fprintf(fptr, "%s", ").");
        fprintf(fptr, "%s", "\n");
    }
    fclose(fptr);
}

int main(int argc, char *argv[]) {
    int n, m, cmd = 0;
    char str_int[4];
    srand(time(NULL));
    printf("Hi!\n"
           "This is the program to generate a set of base matrices needed as input for the Minizinc and ASP models.\n"
           "Card suits are associated to integers:\n"
           "\tHEARTS <--> 1\n"
           "\tCLUBS <--> 2\n"
           "\tSPADES <--> 3\n"
           "\tDIAMONDS <--> 4\n"
           "Blocked cells are associated to 5.\n\n");
    if (argc < 2) {
        printf("Please input the dimension of the matrices:\n"
               "\tn = ");
        scanf("%d", &n);
        printf("Please input the number of matrices you want to generate:\n"
               "\tm = ");
        scanf("%d", &m);
    } else {
        m = 10;
        cmd = 1;
    }
    for(int i = 1; i < argc || !cmd; i++) {
        if (argc > 1)
            n = atoi(argv[i]);
        else
            cmd = 1;
        printf("Generating destination directories:\n");
        char mzn_dir[40] = "./minizinc/data/";
        sprintf(str_int, "%d", n);
        strcat(mzn_dir, "size_");
        strcat(mzn_dir, str_int);
        mkdir(mzn_dir, 0700);
        printf("\tGenerated folder %s\n", mzn_dir);
        char asp_dir[40] = "./asp/data/";
        strcat(asp_dir, "size_");
        strcat(asp_dir, str_int);
        mkdir(asp_dir, 0700);
        printf("\tGenerated folder %s\n", asp_dir);
        printf("----------------------------------------------------------------------\n");
        for (int i = m; i > 0; i--) {
            int blocked, occupied, hearts, clubs, spades, diamonds;
            printf("Generating matrix #%d ...\n", m - i + 1);
            printf("\tGenerating cardinality of sets:\n");
            blocked = (rand() % (n * n / 3)) + 1;
            printf("\t\tRandom number of blocked cells blocks = %d\n", blocked);
            occupied = (rand() % (n * n / 3)) + 1;
            printf("\t\tRandom number of occupied cells occupied = %d\n", occupied);
            hearts = (rand() % (n * n)) + 1;
            printf("\t\tRandom number of hearts cards hearts = %d\n", hearts);
            clubs = (rand() % (n * n)) + 1;
            printf("\t\tRandom number of clubs cards clubs = %d\n", clubs);
            spades = (rand() % (n * n)) + 1;
            printf("\t\tRandom number of spades cards spades = %d\n", spades);
            diamonds = (rand() % (n * n)) + 1;
            printf("\t\tRandom number of diamonds cards diamonds = %d\n", diamonds);
            printf("\tGenerating coordinates for blocked and occupied cells:\n");
            cell *cells = gen_cells(n, blocked, occupied, hearts, clubs, spades, diamonds);
            printf("\t\t");
            for (int l = 0; l < blocked + occupied; l++) {
                printf("| (%d, %d, %d) ", cells[l].x, cells[l].y, cells[l].s);
            }
            printf("|\n");
            printf("\tMatrix #%d:\n", m - i + 1);
            print_matrix(n, blocked, occupied, cells);
            gen_dzn(n, hearts, clubs, spades, diamonds, cells, blocked + occupied, mzn_dir, m - i + 1);
            gen_lp(n, hearts, clubs, spades, diamonds, cells, blocked + occupied, asp_dir, m - i + 1);
            printf("************************************************************\n");
        }
    }
}
