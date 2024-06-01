package com.example.frontend.controllers;

import java.time.LocalDateTime;

public class Report {
    private boolean registries;
    private boolean ram;
    private boolean edr;
    private boolean autopsy;
    private boolean isStatic;
    private LocalDateTime date;

    // Constructor
    public Report(boolean registries, boolean ram, boolean edr, boolean autopsy, LocalDateTime date, boolean isStatic) {
        this.registries = registries;
        this.ram = ram;
        this.edr = edr;
        this.autopsy = autopsy;
        this.date = date;
        this.isStatic = isStatic;
    }

    // Getters and setters
    public boolean isRegistries() {
        return registries;
    }

    public void setRegistries(boolean registries) {
        this.registries = registries;
    }

    public boolean isRam() {
        return ram;
    }

    public void setRam(boolean ram) {
        this.ram = ram;
    }

    public boolean isEdr() {
        return edr;
    }

    public void setEdr(boolean edr) {
        this.edr = edr;
    }

    public boolean isAutopsy() {
        return autopsy;
    }

    public void setAutopsy(boolean autopsy) {
        this.autopsy = autopsy;
    }

    public LocalDateTime getDate() {
        return date;
    }

    public void setDate(LocalDateTime date) {
        this.date = date;
    }

    @Override
    public String toString() {
        return "Report{" +
                "registries=" + registries +
                ", ram=" + ram +
                ", edr=" + edr +
                ", autopsy=" + autopsy +
                ", date=" + date +
                '}';
    }
}
