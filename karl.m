app = App();
fprintf('Starting MATLAB App!\n');

app.register( ...
    @segmentImages, ...
    'segmentImagesdddd', ...
    {app.omeTiffPort('imagePath')}, ...
    {app.omeTiffPort('outputPath')} ...
    );

app.register( ...
    @ZoeSemanticSegmentation, ...
    'ZoeSemanticSegmentation', ...
    {app.omeTiffPort('imagePath')}, ...
    {app.CSVPort('outputPath')} ...
    );

app.register( ...
    @ZoeConstructMesh, ...
    'ZoeConstructMesh', ...
    {app.omeTiffPort('imagePath'), app.CSVPort('csvPath')}, ...
    {app.MeshPort('outputPath')} ...
    );

app.register( ...
    @ZoeGeodesicProjections, ...
    'ZoeGeodesicProjections', ...
    {app.omeTiffPort('imagePath'), app.MeshPort('meshPath')}, ...
    {app.omeTiffPort('outputPath')} ...
    );

fprintf('Apps registered\n');

app.run();
fprintf('App finished\n');

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
    %
    % First step in the pipeline
    %
    addpath("scripts");
    SemanticSegmentation( ...
        "/home/matlab/image.tif", ...
        "/home/matlab", ...
        "unique_name", ...
        1, ...
        100, ...
        0.5, ...
        245, ...
        1000, ...
        "yes" ...
    );
    % Frist Step in the Pipeline
    outputPath = "/home/matlab/semantic_segmentation_points_unique_name.csv";

end

function outputPath = ZoeConstructMesh(imagePath, csvPath)
    %
    % Second step in the pipeline without the pymeshlab call
    %
    addpath('scripts');
    run("scripts/imsaneV1.2/setup.m");
    ConstructMesh( ...
	    "/home/matlab/", ...
        "/home/matlab/", ...
        "/home/matlab", ...
        "image.tif", ...
        "unique_name", ...
        1, ...
        5, ...
        "yes" ...
    );

    % Frist Step in the Pipeline
    outputPath = "/home/matlab/objFiles/pointCloud_unique_name.obj";

end


function outputPath = ZoeGeodesicProjections(imagePath, meshPath)
    %
    % Third step in the pipeline
    %
    addpath("scripts");
    GeodesicProjections( ...
        "/home/matlab/", ...
        "/home/matlab/", ...
        "/home/matlab/image.tif", ...
        "unique_name", ...
        1, ...
        5, ...
        21, ...
        1 ...
    );

    % Frist Step in the Pipeline
    % ToDo Return a list of images not just a single image
    outputPath = "/home/matlab/unique_name/geodesicProjections/atlas/cylinder1/cmp_1_1__T0005.tif";
        % "/home/matlab/unique_name/geodesicProjections/atlas/cylinder1/cmp_1_2__T0005.tif",
        % "/home/matlab/unique_name/geodesicProjections/atlas/cylinder2/cmp_1_1__T0005.tif",
        % "/home/matlab/unique_name/geodesicProjections/atlas/cylinder2/cmp_1_2__T0005.tif"
    % };

end
