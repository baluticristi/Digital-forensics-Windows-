package com.example.frontend.controllers;

import com.example.frontend.MainWindow;
import com.jfoenix.controls.JFXCheckBox;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.scene.paint.CycleMethod;
import javafx.scene.paint.RadialGradient;
import javafx.scene.paint.Stop;
import javafx.scene.shape.Circle;
import javafx.stage.FileChooser;
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
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import org.json.JSONObject;



public class HelloController {

    public Button reportDynamic;
    public ProgressIndicator staticprogress;
    public Button selectImage;
    public Button generateImage;
    public HBox analyzed;
    public Button detail4;
    public Button detail3;
    public Button detail2;
    public Button detail1;
    public JFXCheckBox registreCheckD;
    public JFXCheckBox ramCheckD;
    public JFXCheckBox edrCheckD;
    public JFXCheckBox autopsyCheckD;
    public Button dynamicA;
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

    private Boolean Registre;
    private Boolean Ram;
    private Boolean Edr;
    private Boolean Autopsy;


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
    private Label imageLabel;
    @FXML
    private Button btnWindow4;

    @FXML
    private Button backButton;

    @FXML
    private VBox vBoxContainer;

    @FXML
    private ListView<String> clickableListView;

    @FXML
    private Button staticA;

    @FXML
    private HBox analyzing;
    @FXML
    private ProgressBar progressBar;
    private ObservableList<Report> listReports;

    private static ObservableList<String> listItems;

    @FXML
    private void openWindow1() throws IOException {
        replaceSceneContent("StaticAnalysis.fxml", "Analiza statica");
        primaryStage.setWidth(320);

    }

    @FXML
    private void openWindow2() throws IOException {
        replaceSceneContent("DynamicAnalysis.fxml", "Analiza dinamica");
        primaryStage.setWidth(400);

    }

    @FXML
    private void openWindow3() throws IOException {
        replaceSceneContent("Report.fxml", "Raport");
        primaryStage.setWidth(320);

    }

    @FXML
    private void openWindow4() throws IOException {
        replaceSceneContent("Configurare.fxml", "Configurare");
        primaryStage.setWidth(320);

    }


    @FXML
    private void backFunction() throws IOException {
        replaceSceneContent("Main.fxml", "Digital Forensics");
        primaryStage.setWidth(320);
    }
    @FXML
    private void setSendConfig() throws IOException {


//        URL url = new URL(server_url+"/config");
//
//        JSONObject jsonBody = new JSONObject();
//        jsonBody.put("registre", registreCheck.isSelected());
//        jsonBody.put("ram", ramCheck.isSelected());
//        jsonBody.put("edr", edrCheck.isSelected());
//        jsonBody.put("autopsy", autopsyCheck.isSelected());
//
//        String postResponse = sendPostRequest(url, jsonBody.toString());
//
//        replaceSceneContent("Main.fxml", "MainWindow");
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
            if(listItems==null) {
                listItems = FXCollections.observableArrayList();
                listItems.add("Static 21.05.2024 13:12");
                listItems.add("Dynamic 21.05.2024 12:12");
                listItems.add("Static 20.05.2024 14:12");
                listItems.add("Static 20.05.2024 12:09");
                listItems.add("Dynamic 20.05.2024 09:35");
                listItems.add("Static 19.05.2024 12:12");
                listItems.add("Dynamic 19.05.2024 12:12");
                listItems.add("Static 18.05.2024 14:12");
                listItems.add("Static 17.05.2024 12:09");
                listItems.add("Dynamic 16.05.2024 09:35");
            }
            clickableListView.setItems(listItems);

            clickableListView.setOnMouseClicked((MouseEvent event) -> {
                String selectedItem = clickableListView.getSelectionModel().getSelectedItem();
                if (selectedItem != null) {
                    try {
                        replaceSceneContent("Configurare.fxml", "Raport");
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                }
            });


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
    //Select image from storage method
    @FXML
    private void selectImageFucntion() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Select a static analisys image");
        fileChooser.getExtensionFilters().addAll(
                new FileChooser.ExtensionFilter("Image Files", "*.png", "*.jpg", "*.gif")
        );

        imageLabel.setText(fileChooser.showOpenDialog(primaryStage).getName());
        staticA.setDisable(false);

    }
    @FXML
    private void generateImageFunction() {

        imageLabel.setText("locaWindowsImage.E01");
        staticA.setDisable(false);
    }

    @FXML
    private void analyzeStatic(){
        staticprogress.setVisible(true);
        edrCheck.setDisable(true);
        autopsyCheck.setDisable(true);
        ramCheck.setDisable(true);
        registreCheck.setDisable(true);
        selectImage.setDisable(true);
        generateImage.setDisable(true);

        Timeline timeline = new Timeline(new KeyFrame(Duration.seconds(3)));
        timeline.setOnFinished(event -> {
            staticprogress.setVisible(false);
            staticA.setText("View report");
            staticA.setOnAction(event1 -> {
                try {
                    openStaticReport();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        });
        timeline.play();
//        ReportGenerator generator = new ReportGenerator();
//        Report report = generator.createReport(true);
//        listReports.add(report);
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd.MM.yy HH.mm");
        String formattedDate = "Static " + now.format(formatter);
        listItems.add(formattedDate);
    }

    private void openStaticReport() throws IOException {
        replaceSceneContent("Configurare.fxml", "Configurare");

    }

    @FXML
    private void openDynamicReport() throws IOException {
        replaceSceneContent("Configurare.fxml", "Configurare");
        primaryStage.setWidth(320);

    }
    @FXML
    private void AnalyzeDynamically(){
        analyzing.setVisible(true);
        registreCheckD.setDisable(true);
        ramCheckD.setDisable(true);
        edrCheckD.setDisable(true);
        autopsyCheckD.setDisable(true);
        dynamicA.setDisable(true);


//set the timeline to last 5 seconds
        Timeline timeline = new Timeline(new KeyFrame(Duration.seconds(5)));
        //After the timeline is done, show the report button
        timeline.setOnFinished(event -> {
//            reportDynamic.setText("View report");
            analyzed.setVisible(true);
        });
        timeline.play();
        reportDynamic.setDisable(false);

//        analyzing.setVisible(false);

//        ReportGenerator generator = new ReportGenerator();
//        Report report = generator.createReport(false);
//        listReports.add(report);
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd.MM.yy HH.mm");
        String formattedDate = "Dynamic " + now.format(formatter);
        listItems.add(formattedDate);

    }
    @FXML
    private void stopAnalyze(){
        analyzing.setVisible(false);
        reportDynamic.setOnAction(event -> {
            try {
                openDynamicReport();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
        reportDynamic.setText("View report");

    }
    @FXML
    private void gotoDetails(){
        //open file 1 2 3 4.txt based on int
        //in notepad


            try {
                // The path to the file
                String filePath = "1.txt";

                // Open Notepad with the file
                ProcessBuilder processBuilder = new ProcessBuilder("notepad.exe", filePath);
                processBuilder.start();
            } catch (Exception e) {
                e.printStackTrace();
            }


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