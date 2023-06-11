#include "gtest/gtest.h" // Include the Google Test library
#include <mutex>
#include <condition_variable>

extern "C" {
#include "Add.h" // Include the .c file that contains the function implementation
}

// Define a test for the sumar function
TEST(AddTest, CorrectSum) {
    int result = add(3, 5);
    EXPECT_EQ(result, 8); // Verify that the result is 8
}

// Entry point to run all the tests
int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}






