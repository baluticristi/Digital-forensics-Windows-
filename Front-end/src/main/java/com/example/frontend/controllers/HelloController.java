package com.example.frontend.controllers;

import com.example.frontend.HelloApplication;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import java.io.IOException;

public class HelloController {

    private Stage primaryStage;
    public void setPrimaryStage(Stage primaryStage) {
        this.primaryStage = primaryStage;
    }

    @FXML
    private Button btnWindow1;

    @FXML
    private Button btnWindow2;

    @FXML
    private Button btnWindow3;

    @FXML
    private Button btnWindow4;

    @FXML
    private void openWindow1() throws IOException {
        replaceSceneContent("StaticAnalysis.fxml", "Window 1");
    }
    @FXML
    private void openWindow2() throws IOException {
        replaceSceneContent("DynamicAnalysis.fxml", "Window 2");
    }

    @FXML
    private void openWindow3() throws IOException {
        replaceSceneContent("Report.fxml", "Window 3");
    }

    @FXML
    private void openWindow4() throws IOException {
        replaceSceneContent("Configurare.fxml", "Window 4");
    }
    private void replaceSceneContent(String fxmlFile, String title) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(HelloApplication.class.getResource(fxmlFile));
        Parent newRoot = fxmlLoader.load();
        Scene currentScene = primaryStage.getScene();
        if (currentScene == null) {
            currentScene = new Scene(newRoot);
            primaryStage.setScene(currentScene);
        } else {
            primaryStage.getScene().setRoot(newRoot);
        }
        primaryStage.setTitle(title);
        primaryStage.show();
    }
}