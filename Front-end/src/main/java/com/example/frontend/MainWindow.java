package com.example.frontend;

import com.example.frontend.controllers.HelloController;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import java.io.IOException;
import javafx.scene.image.Image;
public class MainWindow extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(MainWindow.class.getResource("Main.fxml"));
        Parent root = fxmlLoader.load();

        HelloController controller = fxmlLoader.getController();
        controller.setPrimaryStage(stage);

        Image applicationIcon = new Image(MainWindow.class.getResourceAsStream("logo.png"));
        stage.getIcons().add(applicationIcon);
        Scene scene = new Scene(root);
        stage.setTitle("MainApp!");
        stage.setScene(scene);
        stage.show();
    }
}
