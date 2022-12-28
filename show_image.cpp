#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
using namespace cv;
using namespace std;

int main( int argc, char** argv ) {
    if( argc != 2) {
     cout <<" Usage: display_image ImageToLoadAndDisplay" << endl;
     return -1;
    }

    Mat image;
    image = imread(argv[1], IMREAD_LOAD_GDAL);   // Read the file
    if(!image.data ) {                             // Check for invalid input
        cout <<  "Could not open or find the image" << std::endl;
        return -1;
    }

    namedWindow( "Display window", WINDOW_AUTOSIZE );// Create a window.
    imshow( "Display window", image );            // Show our image inside it.

    if (waitKey(10000) == 27) {
        cout << "Esc key is pressed by user. Stoppig the video" << endl;
        // break;   
    }

    return 0;
}
