package com.assigndevelopers;

import java.io.BufferedReader;
import java.io.IOException;

public class ReadFileFilter {
    private final String filePath;

    public ReadFileFilter(String filePath) {
        this.filePath = filePath;
    }

    // Read words from the file
    public String readContent() throws IOException {
        StringBuilder content = new StringBuilder();
        BufferedReader br = new BufferedReader(new java.io.FileReader(filePath));
        String line;

        System.out.println("\nUNIQUE SORTED WORDS:");

        while ((line = br.readLine()) != null) {
            content.append(line).append(" ");
        }
        br.close();
        return content.toString();
    }

}
