#include "dirent.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "time.h"

char *gen_date() {
  char hours[4], minutes[4], seconds[4], day[4], month[4], year[8];
  time_t now;
  time(&now);
  struct tm *local = localtime(&now);
  sprintf(hours, "%02d", local->tm_hour); // get hours since midnight (0-23)
  sprintf(minutes, "%02d",
          local->tm_min); // get minutes passed after the hour (0-59)
  sprintf(seconds, "%02d",
          local->tm_sec); // get seconds passed after a minute (0-59)

  sprintf(day, "%02d", local->tm_mday);      // get day of month (1 to 31)
  sprintf(month, "%02d", local->tm_mon + 1); // get month of year (0 to 11)
  sprintf(year, "%d", local->tm_year + 1900);
  char *dir_name = malloc(40);
  strcat(dir_name, year);
  strcat(dir_name, "_");
  strcat(dir_name, month);
  strcat(dir_name, "_");
  strcat(dir_name, day);
  strcat(dir_name, "_");
  strcat(dir_name, hours);
  strcat(dir_name, "_");
  strcat(dir_name, minutes);
  strcat(dir_name, "_");
  strcat(dir_name, seconds);
  return dir_name;
}

void evaluate_model_and_write_results(FILE *jsonptr, char *file_path, int is_mzn) {
  char line[5000];
  int n, hearts, clubs, spades, diamonds;
  int line_count = 0;
  FILE *dataptr;
  dataptr = fopen(file_path, "r");
  while (fgets(line, 2000, dataptr) != NULL && line_count < 5) {
    line_count += 1;
    char *token = strtok(line, "=");
    token = strtok(NULL, "=");
    if (strncmp(line, "n", 1) == 0 || strncmp(line, "#const n", 8) == 0) {
      n = atoi(token);
      fprintf(jsonptr, "%s", "\t\t\t\t\"n\":");
      fprintf(jsonptr, "%d", n);
      fprintf(jsonptr, "%s", ",\n");
    } else if (strncmp(line, "hearts", 6) == 0 ||
               strncmp(line, "#const hearts", 13) == 0) {
      hearts = atoi(token);
      fprintf(jsonptr, "%s", "\t\t\t\t\"hearts\":");
      fprintf(jsonptr, "%d", hearts);
      fprintf(jsonptr, "%s", ",\n");
    } else if (strncmp(line, "clubs", 5) == 0 ||
               strncmp(line, "#const clubs", 12) == 0) {
      clubs = atoi(token);
      fprintf(jsonptr, "%s", "\t\t\t\t\"clubs\":");
      fprintf(jsonptr, "%d", clubs);
      fprintf(jsonptr, "%s", ",\n");
    } else if (strncmp(line, "spades", 6) == 0 ||
               strncmp(line, "#const spades", 13) == 0) {
      spades = atoi(token);
      fprintf(jsonptr, "%s", "\t\t\t\t\"spades\":");
      fprintf(jsonptr, "%d", spades);
      fprintf(jsonptr, "%s", ",\n");
    } else if (strncmp(line, "diamonds", 6) == 0 ||
               strncmp(line, "#const diamonds", 13) == 0) {
      diamonds = atoi(token);
      fprintf(jsonptr, "%s", "\t\t\t\t\"diamonds\":");
      fprintf(jsonptr, "%d", diamonds);
      fprintf(jsonptr, "%s", ",\n");
    }
  }
  fgets(line, 1000, dataptr);
  line_count = 0;
  int m[n * n], col_count;
  for (int i = 0; i < n * n; i++)
    m[i] = 0;
  if (is_mzn){
    while (line_count < n) {
      col_count = 0;
      fgets(line, 1000, dataptr);
      char *line_ptr = line, trimmed_line[1000] = "";
      line_ptr += 1;
      strncpy(trimmed_line, line_ptr, n * 2 - 1);
      char *token = strtok(trimmed_line, ",");
      while (token != NULL) {
        if (strcmp(token, "_") != 0)
          m[line_count * n + col_count] = atoi(token);
        token = strtok(NULL, ",");
        col_count += 1;
      }
      line_count += 1;
    }
  }
  else
    do {
      int tuple_len = strlen(line) - 10;
      char *tuple = (char *)malloc(sizeof(char) * (tuple_len + 1));
      strncpy(tuple, line + 8, tuple_len);
      int x = atoi(strtok(tuple, ",")) - 1;
      int y = atoi(strtok(NULL, ",")) - 1;
      int s = atoi(strtok(NULL, ","));
      m[x * n + y] = s;
    } while (fgets(line, 1000, dataptr) != NULL);

  fprintf(jsonptr, "%s", "\t\t\t\t\"m\": [");
  for (int i = 0; i < n * n; i++) {
    fprintf(jsonptr, "%d", m[i]);
    if (i == n * n - 1)
      fprintf(jsonptr, "%s", "],\n");
    else
      fprintf(jsonptr, "%s", ", ");
  }

  char mzn_command[1000] =
      "minizinc ./minizinc/config.mpc ./minizinc/model.mzn ";
  char asp_command[1000] = "clingo --time-limit 300 --configuration=jumpy --restart-on-model -t 8,split ";
  char command[1000];
  if (is_mzn) {
    strcpy(command, mzn_command);
    strcat(command, file_path);
  } else {
    strcpy(command, asp_command);
    strcat(command, file_path);
    strcat(command, " ./asp/model.lp");
  }

  clock_t start = clock_gettime_nsec_np(CLOCK_MONOTONIC);
  fprintf(jsonptr, "%s", "\t\t\t\t\"steps\":[\n");
  FILE *shptr = popen(command, "r");
  int step_count = 1;
  while (fgets(line, 2000, shptr) != NULL) {
    printf("%s", line);
    if (step_count != 1 && strncmp(line, "griglia", 7) == 0)
      fprintf(jsonptr, "%s", ",\n");
    if (strncmp(line, "griglia", 7) == 0) {
      fprintf(jsonptr, "%s", "\t\t\t\t\t{\n\t\t\t\t\t\"step\": ");
      fprintf(jsonptr, "%d", step_count);
      fprintf(jsonptr, "%s", ",\n");
      char *save_ptr1, *save_ptr2;
      char *token = strtok_r(line, " ", &save_ptr1);
      while (token != NULL) {
        if (strncmp(token, "griglia", 7) == 0) {
          int tuple_len = strlen(token) - 9;
          char *tuple = (char *)malloc(sizeof(char) * (tuple_len + 1));
          strncpy(tuple, token + 8, tuple_len);
          int x = atoi(strtok_r(tuple, ",", &save_ptr2)) - 1;
          int y = atoi(strtok_r(NULL, ",", &save_ptr2)) - 1;
          int s = atoi(strtok_r(NULL, ",", &save_ptr2));
          m[x * n + y] = s;
        }
        token = strtok_r(NULL, " ", &save_ptr1);
      }
      fprintf(jsonptr, "%s", "\t\t\t\t\t\t\"m\": [");
      for (int i = 0; i < n * n; i++) {
        fprintf(jsonptr, "%d", m[i]);
        if (i == n * n - 1)
          fprintf(jsonptr, "%s", "],\n");
        else
          fprintf(jsonptr, "%s", ", ");
      }
      step_count += 1;
    } else if (strncmp(line, "Optimization:", 13) == 0) {
      strtok(line, " ");
      int score = atoi(strtok(NULL, " "));
      if (!is_mzn)
        score *= -1;
      fprintf(jsonptr, "%s", "\t\t\t\t\t\t\"score\": ");
      fprintf(jsonptr, "%d", score);
      fprintf(jsonptr, "%s", "\n");
      fprintf(jsonptr, "%s", "\t\t\t\t\t}");
    }
  }
  fprintf(jsonptr, "%s", "\n\t\t\t\t],\n");
  clock_t end = clock_gettime_nsec_np(CLOCK_MONOTONIC);
  double time_spent = (double)(end - start) / 10e8;
  fprintf(jsonptr, "%s", "\t\t\t\t\"execution_time\":");
  fprintf(jsonptr, "%.4f", time_spent);
  fprintf(jsonptr, "%s", "\n");
}

int main(int argc, char **argv) {
  setbuf(stdout, NULL);
  FILE *jsonptr;
  char result_file[100] = "./results/results_";
  strcat(result_file, gen_date());
  strcat(result_file, ".json");
  jsonptr = fopen(result_file, "w");
  fprintf(jsonptr, "%s", "{\n");

  for (int i = 1; i < argc; i++) {
    int file_count = 0;
    char *dir_name = argv[i];
    char mzn_dir_path[100] = "./minizinc/data/";
    char asp_dir_path[100] = "./asp/data/";
    strcat(mzn_dir_path, dir_name);
    strcat(asp_dir_path, dir_name);
    char *token = strtok(dir_name, "_");
    token = strtok(NULL, "_");
    fprintf(jsonptr, "%s%d%s", "\t\"", atoi(token), "\":{\n");

    DIR *mzn_dir, *asp_dir;
    struct dirent *mzn_dirent, *asp_dirent;
    mzn_dir = opendir(mzn_dir_path);
    asp_dir = opendir(asp_dir_path);

    fprintf(jsonptr, "%s", "\t\t\"mzn\":{\n");
    while ((mzn_dirent = readdir(mzn_dir)) != NULL) {
      if (mzn_dirent->d_type == DT_REG) {
        file_count += 1;
        int file_number = atoi(mzn_dirent->d_name);
        printf(".-----------------------------------------------------.\n"
               "| MiniZinc: working on size %d with data file %s|\n"
               "'-----------------------------------------------------'\n",
               atoi(token), mzn_dirent->d_name);
        char mzn_file_path[100];
        strcpy(mzn_file_path, mzn_dir_path);
        strcat(mzn_file_path, "/");
        strcat(mzn_file_path, mzn_dirent->d_name);
        fprintf(jsonptr, "%s%d%s", "\t\t\t\"", file_number, "\":{\n");
        evaluate_model_and_write_results(jsonptr, mzn_file_path, 1);
        if (file_count < 20)
          fprintf(jsonptr, "%s", "\t\t\t},\n");
        else
          fprintf(jsonptr, "%s", "\t\t\t}\n");
      }
    }
    fprintf(jsonptr, "%s", "\t\t},\n");

    fprintf(jsonptr, "%s", "\t\t\"asp\":{\n");
    file_count = 0;
    while ((asp_dirent = readdir(asp_dir)) != NULL) {
      if (asp_dirent->d_type == DT_REG) {
        file_count += 1;
        int file_number = atoi(asp_dirent->d_name);
        printf(".-----------------------------------------.\n"
               "| ASP: working on size %d on data file %s |\n"
               "'-----------------------------------------'\n",
               atoi(token), asp_dirent->d_name);
        char asp_file_path[100];
        strcpy(asp_file_path, asp_dir_path);
        strcat(asp_file_path, "/");
        strcat(asp_file_path, asp_dirent->d_name);
        fprintf(jsonptr, "%s%d%s", "\t\t\t\"", file_number, "\":{\n");
        evaluate_model_and_write_results(jsonptr, asp_file_path, 0);
        if (file_count < 20)
          fprintf(jsonptr, "%s", "\t\t\t},\n");
        else
          fprintf(jsonptr, "%s", "\t\t\t}\n");
      }
    }
    fprintf(jsonptr, "%s", "\t\t}\n");
    if (i < argc - 1)
      fprintf(jsonptr, "%s", "\t},\n");
    else
      fprintf(jsonptr, "%s", "\t}\n");
  }
  fprintf(jsonptr, "%s", "}");
  fclose(jsonptr);
}
