package com.assigndevelopers;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Set;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        //TIP Press <shortcut actionId="ShowIntentionActions"/> with your caret at the highlighted text
        // to see how IntelliJ IDEA suggests fixing it.<br>

        //TIP Press <shortcut actionId="Debug"/> to start debugging your code. We have set one <icon src="AllIcons.Debugger.Db_set_breakpoint"/> breakpoint
        // for you, but you can always add more by pressing <shortcut actionId="ToggleLineBreakpoint"/>.<br>
        // java -cp pipe_filter_app-1.0-SNAPSHOT.jar com.assigndevelopers.Main <br>
        // java -jar target/pipe_filter_app-1.0-SNAPSHOT.jar <br>
        // java -jar pipe_filter_app-1.0-SNAPSHOT.jar

        InputFilter inputFilter = new InputFilter();
        try {
            String filePath = inputFilter.askUser();

            // If the file path is provided in the console, use it directly
            if (!(new File(filePath)).exists()) {
                System.out.println("File not found: " + filePath);
                return;
            }

            ReadFileFilter readFileFilter = new ReadFileFilter(filePath);
            WordFilter wordFilter = new WordFilter();
            UniqueFilter uniqueFilter = new UniqueFilter();
            SortFilter sortFilter = new SortFilter();
            OutputFilter outputFilter = new OutputFilter();

            // Processing Text
            String content = readFileFilter.readContent();
            List<String> splitWords = wordFilter.splitWords(content);
            Set<String> uniqueWords = uniqueFilter.removeDuplicates(splitWords);
            List<String> sortedWords = sortFilter.sortWords(uniqueWords);
            // Show output of distinct words
            outputFilter.printWords(sortedWords);

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            inputFilter.scanner.close();
        }
    }
}