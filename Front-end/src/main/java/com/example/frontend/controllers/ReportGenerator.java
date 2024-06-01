package com.example.frontend.controllers;
import java.time.LocalDateTime;

public class ReportGenerator {

    public Report createReport(Boolean isStatic) {
        // Logic to determine the boolean values for the report
        boolean registries = checkRegistries();
        boolean ram = checkRam();
        boolean edr = checkEdr();
        boolean autopsy = checkAutopsy();
        boolean staticA = isStatic;
        // Capture the current date and time
        LocalDateTime now = LocalDateTime.now();

        // Create and return the Report object
        return new Report(registries, ram, edr, autopsy, now, staticA);
    }

    private boolean checkRegistries() {
        // Placeholder logic for determining the value
        return true; // or some actual condition
    }

    private boolean checkRam() {
        // Placeholder logic for determining the value
        return false; // or some actual condition
    }

    private boolean checkEdr() {
        // Placeholder logic for determining the value
        return true; // or some actual condition
    }

    private boolean checkAutopsy() {
        // Placeholder logic for determining the value
        return false; // or some actual condition
    }

/*    public static void main(String[] args) {
        ReportGenerator generator = new ReportGenerator();
        Report report = generator.createReport();
        System.out.println(report);
    }*/
}
