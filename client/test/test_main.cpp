#include <unity.h>

void setUp(void) {
    // set stuff up here
}

void tearDown(void) {
    // clean stuff up here
}

void test_dummy(void) {
    TEST_ASSERT_TRUE_MESSAGE(true, "This test is dumb");
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_dummy);
    UNITY_END();

    return 0;
}
