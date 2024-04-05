package com.example.frontend.controllers;

import com.example.frontend.MainWindow;
import com.jfoenix.controls.JFXCheckBox;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.image.ImageView;
import javafx.scene.paint.CycleMethod;
import javafx.scene.paint.RadialGradient;
import javafx.scene.paint.Stop;
import javafx.scene.shape.Circle;
import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import java.io.IOException;
import javafx.collections.ObservableList;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.VBox;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.util.Duration;
import javafx.animation.KeyValue;
import javafx.application.Platform;

import java.net.URL;
import java.net.HttpURLConnection;
import java.io.OutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.json.JSONObject;
import org.json.JSONArray;




public class HelloController {

    private String server_url ="http://127.0.0.1:5000";
    public Label staticStatus;
    public ProgressBar cpuProgressBar;
    public ProgressBar memoryProgressBar;
    public ProgressBar diskProgressBar;
    public ProgressBar networkProgressBar;
    public Label optionsLabel;
    public JFXCheckBox registreCheck;
    public JFXCheckBox ramCheck;
    public JFXCheckBox edrCheck;
    public JFXCheckBox autopsyCheck;
    private Stage primaryStage;

    public void setPrimaryStage(Stage primaryStage) {
        this.primaryStage = primaryStage;
    }

    @FXML
    private Button sendConfig;

    @FXML
    private Button btnWindow1;

    @FXML
    private Button btnWindow2;

    @FXML
    private Button btnWindow3;

    @FXML
    private Button btnWindow4;

    @FXML
    private Button backButton;

    @FXML
    private VBox vBoxContainer;

    @FXML
    private ListView<String> clickableListView;

    @FXML
    private ProgressBar progressBar;
    private ObservableList<String> listItems;

    @FXML
    private void openWindow1() throws IOException {
        replaceSceneContent("StaticAnalysis.fxml", "Analiza statica");
    }

    @FXML
    private void openWindow2() throws IOException {
        replaceSceneContent("DynamicAnalysis.fxml", "Analiza dinamica");
    }

    @FXML
    private void openWindow3() throws IOException {
        replaceSceneContent("Report.fxml", "Raport");
    }

    @FXML
    private void openWindow4() throws IOException {
        replaceSceneContent("Configurare.fxml", "Configurare");
    }

    @FXML
    private void backFunction() throws IOException {
        replaceSceneContent("Main.fxml", "MainWindow");
    }
    @FXML
    private void setSendConfig() throws IOException {
        URL url = new URL(server_url+"/config");

        JSONObject jsonBody = new JSONObject();
        jsonBody.put("registre", registreCheck.isSelected());
        jsonBody.put("ram", ramCheck.isSelected());
        jsonBody.put("edr", edrCheck.isSelected());
        jsonBody.put("autopsy", autopsyCheck.isSelected());

        String postResponse = sendPostRequest(url, jsonBody.toString());

        replaceSceneContent("Main.fxml", "MainWindow");
    }
    private void replaceSceneContent(String fxmlFile, String title) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(MainWindow.class.getResource(fxmlFile));
        Parent newRoot = fxmlLoader.load();


        Scene currentScene = primaryStage.getScene();
        if (currentScene == null) {
            currentScene = new Scene(newRoot);
            primaryStage.setScene(currentScene);
        } else {
            primaryStage.getScene().setRoot(newRoot);
        }
        primaryStage.setTitle(title);
        HelloController controller = fxmlLoader.getController();
        controller.setPrimaryStage(primaryStage);
        primaryStage.show();
    }


    @FXML
    private ImageView logoImageView;

    @FXML
    public void initialize() throws IOException {
        // Define the radial gradient
        if (logoImageView != null) {
            RadialGradient gradient = new RadialGradient(
                    0,      // focusAngle
                    .1,     // focusDistance
                    50,     // centerX
                    50,     // centerY
                    50,     // radius
                    false,
                    CycleMethod.NO_CYCLE, // cycleMethod
                    new Stop(0, javafx.scene.paint.Color.WHITE), // stops
                    new Stop(1, javafx.scene.paint.Color.TRANSPARENT)
            );


            // Create a circle clip
            Circle clipCircle = new Circle(50, 50, 50);
            clipCircle.setFill(gradient);

            // Apply the clip to the ImageView
            logoImageView.setClip(clipCircle);
        }
        if(clickableListView !=null)
        {
            listItems = FXCollections.observableArrayList();
            clickableListView.setItems(listItems);


            clickableListView.setOnMouseClicked((MouseEvent event) -> {
                String selectedItem = clickableListView.getSelectionModel().getSelectedItem();
                if (selectedItem != null) {
                    // Handle the click event for the selected item
                    handleItemClick(selectedItem);
                }
            });

            URL getUrl = new URL(server_url +"/rapoarte");

            String getResponse = sendGetRequest(getUrl);
            JSONObject jsonResponse = new JSONObject(getResponse);
            String jsonString = jsonResponse.optString("reports");
            JSONArray jsonArray = new JSONArray(jsonString);

            for (int i = 0; i < jsonArray.length(); i++) {
                appendItemToList(jsonArray.getString(i));

            }
        }
        if(optionsLabel != null)
        {
            URL getUrl = new URL(server_url +"/config");

            String getResponse = sendGetRequest(getUrl);
            JSONObject jsonResponse = new JSONObject(getResponse);
            Boolean registre = Boolean.valueOf(jsonResponse.optString("registre"));
            Boolean ram = Boolean.valueOf(jsonResponse.optString("ram"));
            Boolean edr = Boolean.valueOf(jsonResponse.optString("edr"));
            Boolean autopsy = Boolean.valueOf(jsonResponse.optString("autopsy"));

            registreCheck.setSelected(registre);
            ramCheck.setSelected(ram);
            edrCheck.setSelected(edr);
            autopsyCheck.setSelected(autopsy);
        }

    }



    public void appendItemToList(String item) {
        listItems.add(item);
    }

    private void handleItemClick(String item) {
        Tooltip tooltip = new Tooltip("Clicked on item: " + item);

        tooltip.show(clickableListView.getScene().getWindow(),
                clickableListView.localToScreen(clickableListView.getBoundsInLocal()).getMinX(),
                clickableListView.localToScreen(clickableListView.getBoundsInLocal()).getMinY());

        Timeline timeline = new Timeline(new KeyFrame(Duration.seconds(1), evt -> tooltip.hide()));
        timeline.play();
    }

    @FXML
    private void runProgressBar() {
        progressBar.setProgress(0);

        Duration duration = Duration.seconds(3);

        KeyValue keyValue = new KeyValue(progressBar.progressProperty(), 1);

        KeyFrame keyFrame = new KeyFrame(duration, event ->{
            staticStatus.setText("You can view the report in reports!");
        } ,keyValue);
        Timeline timeline = new Timeline(keyFrame);

        timeline.play();
        handleSendRequest();

    }

    public void handleSendRequest() {
        // Run the network request in a separate thread to avoid freezing the UI
        new Thread(() -> {
            try {
                // Replace with your server's URL and the data you want to post
                URL url = new URL(server_url+"/");

                // Create the request body, content-type can be "application/json" or other types depending on your needs
                JSONObject jsonBody = new JSONObject();
                jsonBody.put("key1", "value1");
                jsonBody.put("key2", "value2");

                String postResponse = sendPostRequest(url, jsonBody.toString());

                JSONObject jsonResponse = new JSONObject(postResponse);

                if ("OK".equals(jsonResponse.optString("message"))) {
                    URL getUrl = new URL(server_url+"/raport");

                   // String getResponse = sendGetRequest(getUrl);
                    Platform.runLater(() -> staticStatus.setText("Data sent successfully!"));
                } else {
                    Platform.runLater(() -> staticStatus.setText("POST request did not return {'message': 'OK'}"));
                }
            } catch (Exception e) {
                e.printStackTrace();
                Platform.runLater(() -> staticStatus.setText("Error: " + e.getMessage()));
            }
        }).start();
    }

    private String sendPostRequest(URL url, String requestBody) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json; utf-8");
        connection.setRequestProperty("Accept", "application/json");
        connection.setDoOutput(true);

        // Send the POST request with the JSON body
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = requestBody.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        // Read the response
        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(connection.getInputStream(), "utf-8"))) {
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
        }

        connection.disconnect();
        return response.toString();
    }

    private String sendGetRequest(URL url) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(connection.getInputStream(), "utf-8"))) {
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
        }

        connection.disconnect();
        return response.toString();
    }


}