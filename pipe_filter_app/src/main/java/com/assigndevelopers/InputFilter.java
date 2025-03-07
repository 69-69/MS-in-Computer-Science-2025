package com.assigndevelopers;

import java.util.Scanner;

public class InputFilter {
    public Scanner scanner = new Scanner(System.in);

    // Ask the user if they want to use the default file or provide a custom file path
    public String askUser() {
        String inputFile = "src/main/resources/problem_3_test_file.txt";

        System.out.print("\nEnter 1 to use the Default File, or 2 for your File Path: ");

        int choice = scanner.nextInt();
        scanner.nextLine();

        // Handle user input
        if (choice == 1) {
            // Default file path
            System.out.println("Using default file: " + inputFile);
        } else if (choice == 2) {
            // Ask user to input custom file path
            System.out.print("Please paste the full file path: ");
            inputFile = scanner.nextLine();
            System.out.println("Using provided file: " + inputFile);
        } else {
            // Invalid input handling
            System.out.println("Invalid choice. Using default file path.");
        }

        return inputFile;
    }
}
