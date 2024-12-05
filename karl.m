app = App();

fprintf('Hello from MATLAB!\n');

app.register(@segmentImages, 'segmentImagesdddd', {app.omeTiffPort('imagePath')}, {app.omeTiffPort('outputPath')});

app.register(@ZoeSegmenticSegmentation, 'ZoeSemanticSegmentation', {app.omeTiffPort('imagePath')}, {app.omeTiffPort('outputPath')});

fprintf('Apps registered\n');
app.run();
fprintf('App closed\n');

function outputPath = segmentImages(imagePath)

    % Read a TIFF file and print the maximum value


    % Read the TIFF image
    image_data = imread(imagePath);


    % Compute the maximum value
    max_value = max(image_data(:));

    % Print the maximum value
    fprintf('The maximum pixel value in the image is: %d\n', max_value);

    % Return the processed image path
    outputPath = imagePath;
end

function outputPath = ZoeSemanticSegmentation(imagePath)

    addpath("scripts");
    SemanticSegmentation( ...
	tifFile, ...
	csvDir, ...
	parameters.uniqueName, ...
	parameters.semseg.beadthresh, ...
	parameters.semseg.beadradius, ...
	parameters.semseg.BWthreshMan, ...
	parameters.semseg.alpha, ...
	parameters.semseg.alphaRegionThreshold, ...
	parameters.createMesh ...
    );
    % Frist Step in the Pipeline
    outputPath = csvPath;

end
