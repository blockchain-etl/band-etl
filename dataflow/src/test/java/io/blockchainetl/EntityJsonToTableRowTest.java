package io.blockchainetl;

import io.blockchainetl.band.fns.EntityJsonToTableRow;
import org.junit.Test;

import java.io.IOException;
import java.net.URL;
import java.nio.file.Files;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertLinesMatch;

public class EntityJsonToTableRowTest {
    private final EntityJsonToTableRow converter = new EntityJsonToTableRow();

    @Test
    public void testBlockConversion() throws Exception {
        test("testdata/TransactionJsonToTableRowTest/inputBlocks.txt",
            "testdata/TransactionJsonToTableRowTest/expectedBlocks.txt");
    }

    @Test
    public void testActionConversion() throws Exception {
        test("testdata/TransactionJsonToTableRowTest/inputTransactions.txt",
            "testdata/TransactionJsonToTableRowTest/expectedTransactions.txt");
    }

    @Test
    public void testLogConversion() throws Exception {
        test("testdata/TransactionJsonToTableRowTest/inputLogs.txt",
            "testdata/TransactionJsonToTableRowTest/expectedLogs.txt");
    }

    @Test
    public void testMessageConversion() throws Exception {
        test("testdata/TransactionJsonToTableRowTest/inputMessages.txt",
                "testdata/TransactionJsonToTableRowTest/expectedMessages.txt");
    }

    @Test
    public void testBlockEventConversion() throws Exception {
        test("testdata/TransactionJsonToTableRowTest/inputBlockEvents.txt",
                "testdata/TransactionJsonToTableRowTest/expectedBlockEvents.txt");
    }

    @Test
    public void testOracleRequestConversion() throws Exception {
        test("testdata/TransactionJsonToTableRowTest/inputOracleRequests.txt",
                "testdata/TransactionJsonToTableRowTest/expectedOracleRequests.txt");
    }
    
    private void test(String inputFile, String expectedFile) throws Exception {
        // Given
        List<String> input = readFileLines(inputFile);
        List<String> expected = readFileLines(expectedFile);

        // when
        List<String> actual = input.stream()
            .map(converter::apply)
            .map(com.google.api.services.bigquery.model.TableRow::toString)
            .collect(java.util.stream.Collectors.toList());

        // then
        assertLinesMatch(expected, actual);
    }

    private List<String> readFileLines(String fileName) throws IOException {
        URL resource = this.getClass().getClassLoader().getResource(fileName);
        if (resource == null) {
            throw new IOException("Resource not found: " + fileName);
        }
        return Files.readAllLines(
            java.nio.file.Paths.get(resource.getPath()));
    }
}
