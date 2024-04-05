module com.example.frontend {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.kordamp.bootstrapfx.core;
    requires org.json;
    requires com.jfoenix;

    opens com.example.frontend to javafx.fxml;
    exports com.example.frontend;
    exports com.example.frontend.controllers;
    opens com.example.frontend.controllers to javafx.fxml;
}