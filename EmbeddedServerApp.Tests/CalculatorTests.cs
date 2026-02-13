using EmbeddedServerApp.Models;
using Xunit;

namespace EmbeddedServerApp.Tests
{
    public class CalculatorTests
    {
        [Theory]
        [InlineData(1, 2, 3)]
        [InlineData(-1, 1, 0)]
        [InlineData(0, 0, 0)]
        public void Add_Works(double a, double b, double expected)
        {
            Assert.Equal(expected, Calculator.Add(a, b));
        }

        [Theory]
        [InlineData(5, 2, 3)]
        [InlineData(0, 1, -1)]
        public void Subtract_Works(double a, double b, double expected)
        {
            Assert.Equal(expected, Calculator.Subtract(a, b));
        }

        [Theory]
        [InlineData(2, 3, 6)]
        [InlineData(-2, 2, -4)]
        public void Multiply_Works(double a, double b, double expected)
        {
            Assert.Equal(expected, Calculator.Multiply(a, b));
        }

        [Theory]
        [InlineData(6, 2, 3)]
        [InlineData(1, 0, double.NaN)]
        public void Divide_Works(double a, double b, double expected)
        {
            Assert.Equal(expected, Calculator.Divide(a, b));
        }
    }
}
