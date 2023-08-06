import unittest
from unittest.mock import MagicMock, call, patch

from uniquorn import Uniquorn


class TestUniquornParameterOrderNotProtected(unittest.TestCase):

    def test_name_not_in_order_protection(self):
        """not found == not protected"""
        name = "not found"
        for order_protection in ["foo", "bar", "bas"], ("foo", "bar", "bas"), {"foo", "bar", "bas"}:
            #
            actual = Uniquorn._uniquorn_parameter_order_not_protected(Uniquorn, name, order_protection)
            #
            expect = True
            self.assertEqual(expect, actual)

    def test_name_in_order_protection(self):
        """found != not protected"""
        name = "bar"
        for order_protection in ["foo", "bar", "bas"], ("foo", "bar", "bas"), {"foo", "bar", "bas"}:
            #
            actual = Uniquorn._uniquorn_parameter_order_not_protected(Uniquorn, name, order_protection)
            #
            expect = False
            self.assertEqual(expect, actual)

    def test_order_protection_true(self):
        """True protects everything"""
        name = "everything"
        order_protection = True
        #
        actual = Uniquorn._uniquorn_parameter_order_not_protected(Uniquorn, name, order_protection)
        #
        expect = False
        self.assertEqual(expect, actual)

    def test_order_protection_not_true(self):
        """not True protects nothing"""
        name = "nothing"
        for order_protection in False, None, 1:
            #
            actual = Uniquorn._uniquorn_parameter_order_not_protected(Uniquorn, name, order_protection)
            #
            expect = True
            self.assertEqual(expect, actual, msg=f"""failed for {order_protection=}""")


class TestUniquornParameterOrderNotProtectedThroughAttribute(unittest.TestCase):

    def test_attribute_exists(self):
        """next step iff attribute exists"""
        cls = MagicMock()
        cls.attribute = "MOCK attribute value"
        cls._uniquorn_parameter_order_not_protected.return_value = "MOCK called"
        name = "parameter name"
        order_protection_attribute_name = "attribute"
        #
        actual = Uniquorn._uniquorn_parameter_order_not_protected_through_attribute(
            cls,
            name,
            order_protection_attribute_name,
        )
        #
        expect = "MOCK called"
        self.assertEqual(expect, actual)
        expect = [
            call._uniquorn_parameter_order_not_protected("parameter name", "MOCK attribute value")
        ]
        self.assertListEqual(expect, cls.mock_calls)

    def test_attribute_does_not_exists(self):
        """direct result iff attribute does not exist"""
        cls = MagicMock()
        del cls.attribute
        cls._uniquorn_parameter_order_not_protected.return_value = "MOCK called"
        name = "parameter name"
        order_protection_attribute_name = "attribute"
        #
        actual = Uniquorn._uniquorn_parameter_order_not_protected_through_attribute(
            cls,
            name,
            order_protection_attribute_name,
        )
        #
        expect = True
        self.assertEqual(expect, actual)
        expect = []
        self.assertListEqual(expect, cls.mock_calls)


class TestUniquornCanonicalParameterValue(unittest.TestCase):

    def test_list_value_not_protected(self):
        cls = MagicMock()
        cls._uniquorn_parameter_order_not_protected_through_attribute.return_value = True
        name = "parameter name"
        value = ["b", "c", "a"]
        #
        actual = Uniquorn._uniquorn_canonical_parameter_value(cls, name, value)
        #
        expect = ["a", "b", "c"]
        self.assertListEqual(expect, actual)
        expect = [
            call._uniquorn_parameter_order_not_protected_through_attribute(
                "parameter name",
                "uniquorn_list_order_matters",
            ),
        ]
        self.assertListEqual(expect, cls.mock_calls)

    def test_list_value_protected(self):
        cls = MagicMock()
        cls._uniquorn_parameter_order_not_protected_through_attribute.return_value = False
        name = "parameter name"
        value = ["b", "c", "a"]
        #
        actual = Uniquorn._uniquorn_canonical_parameter_value(cls, name, value)
        #
        expect = ["b", "c", "a"]
        self.assertListEqual(expect, actual)
        expect = [
            call._uniquorn_parameter_order_not_protected_through_attribute(
                "parameter name",
                "uniquorn_list_order_matters",
            ),
        ]
        self.assertListEqual(expect, cls.mock_calls)

    def test_dict_value_not_protected(self):
        cls = MagicMock()
        cls._uniquorn_parameter_order_not_protected_through_attribute.return_value = True
        name = "parameter name"
        value = {"b": 0, "c": 1, "a": 2}
        #
        actual = Uniquorn._uniquorn_canonical_parameter_value(cls, name, value)
        #
        expect = {"a": 2, "b": 0, "c": 1}
        self.assertDictEqual(expect, actual)
        expect = [
            call._uniquorn_parameter_order_not_protected_through_attribute(
                "parameter name",
                "uniquorn_dict_order_matters",
            ),
        ]
        self.assertListEqual(expect, cls.mock_calls)

    def test_dict_value_protected(self):
        cls = MagicMock()
        cls._uniquorn_parameter_order_not_protected_through_attribute.return_value = False
        name = "parameter name"
        value = {"b": 0, "c": 1, "a": 2}
        #
        actual = Uniquorn._uniquorn_canonical_parameter_value(cls, name, value)
        #
        expect = {"b": 0, "c": 1, "a": 2}
        self.assertDictEqual(expect, actual)
        expect = [
            call._uniquorn_parameter_order_not_protected_through_attribute(
                "parameter name",
                "uniquorn_dict_order_matters",
            ),
        ]
        self.assertListEqual(expect, cls.mock_calls)


class TestUniquornCreation(unittest.TestCase):

    class UniquornTestClass1(metaclass=Uniquorn):

        def __init__(self, a):
            self.a = a

    class UniquornTestClass2(metaclass=Uniquorn):

        uniquorn_list_order_matters = []
        uniquorn_dict_order_matters = []

        def __init__(self, a, b):
            self.a = a
            self.b = b

    def test_create_0_args(self):
        """__init__ like it should"""
        with self.assertRaises(TypeError):
            instance = TestUniquornCreation.UniquornTestClass1()
        with self.assertRaises(TypeError):
            instance = TestUniquornCreation.UniquornTestClass2()

    def test_create_1_arg(self):
        """__init__ like it should"""
        instance = TestUniquornCreation.UniquornTestClass1("a")
        self.assertEqual("a", instance.a)
        with self.assertRaises(TypeError):
            instance = TestUniquornCreation.UniquornTestClass2()

    def test_create_2_args(self):
        """__init__ like it should"""
        with self.assertRaises(TypeError):
            instance = TestUniquornCreation.UniquornTestClass1("a", "b")
        instance = TestUniquornCreation.UniquornTestClass2("a", "b")
        self.assertEqual("a", instance.a)
        self.assertEqual("b", instance.b)

    def test_create_twice_01(self):
        """identical arguments lead to same instance"""
        for a in ("arg", 1, [], {}):
            instance1 = TestUniquornCreation.UniquornTestClass1(a)
            instance2 = TestUniquornCreation.UniquornTestClass1(a)
            self.assertIs(instance1, instance2, msg=f"failed for {a!r}")

    def test_create_twice_02(self):
        """identical arguments -> same instance"""
        for a in ("arg", 1, [], {}):
            instance1 = TestUniquornCreation.UniquornTestClass1(a=a)
            instance2 = TestUniquornCreation.UniquornTestClass1(a=a)
            self.assertIs(instance1, instance2, msg=f"failed for {a!r}")

    def test_create_twice_03(self):
        """identical arguments -> same instance"""
        for a in ("arg", 1, [], {}):
            instance1 = TestUniquornCreation.UniquornTestClass1(a)
            instance2 = TestUniquornCreation.UniquornTestClass1(a=a)
            self.assertIs(instance1, instance2, msg=f"failed for {a!r}")

    def test_registration(self):
        """instances registered per class"""
        instance1 = TestUniquornCreation.UniquornTestClass1("a1")
        instance2 = TestUniquornCreation.UniquornTestClass2("a2", "b2")
        #
        self.assertIn("a=a1", TestUniquornCreation.UniquornTestClass1._uniquorn_instances)
        self.assertNotIn("a=a2, b=b2", TestUniquornCreation.UniquornTestClass1._uniquorn_instances)
        self.assertIs(instance1, TestUniquornCreation.UniquornTestClass1._uniquorn_instances["a=a1"])
        #
        self.assertIn("a=a2, b=b2", TestUniquornCreation.UniquornTestClass2._uniquorn_instances)
        self.assertNotIn("a=a1", TestUniquornCreation.UniquornTestClass2._uniquorn_instances)
        self.assertIs(instance2, TestUniquornCreation.UniquornTestClass2._uniquorn_instances["a=a2, b=b2"])

    def test_unique_list_01(self):
        """one instance even if list order is different"""
        instance1 = TestUniquornCreation.UniquornTestClass1(["a", "0"])
        instance2 = TestUniquornCreation.UniquornTestClass1(["0", "a"])
        self.assertIs(instance1, instance2)

    def test_unique_list_02(self):
        """two instances if list order is important, one if it's not"""
        with patch.object(TestUniquornCreation.UniquornTestClass2, "uniquorn_list_order_matters", ["a"]):
            instance1 = TestUniquornCreation.UniquornTestClass2(["a", "0"], "b")
            instance2 = TestUniquornCreation.UniquornTestClass2(["0", "a"], "b")
            self.assertIsNot(instance1, instance2)
            #
            instance1 = TestUniquornCreation.UniquornTestClass2("a", ["0", "b"])
            instance2 = TestUniquornCreation.UniquornTestClass2("a", ["b", "0"])
            self.assertIs(instance1, instance2)

        with patch.object(TestUniquornCreation.UniquornTestClass2, "uniquorn_list_order_matters", ["b"]):
            instance1 = TestUniquornCreation.UniquornTestClass2(["a", "0"], "b")
            instance2 = TestUniquornCreation.UniquornTestClass2(["0", "a"], "b")
            self.assertIs(instance1, instance2)
            #
            instance1 = TestUniquornCreation.UniquornTestClass2("a", ["0", "b"])
            instance2 = TestUniquornCreation.UniquornTestClass2("a", ["b", "0"])
            self.assertIsNot(instance1, instance2)

    def test_unique_dict_01(self):
        """one instance even if dict order is different"""
        instance1 = TestUniquornCreation.UniquornTestClass1({"a": 1, "0": 0})
        instance2 = TestUniquornCreation.UniquornTestClass1({"0": 0, "a": 1})
        self.assertIs(instance1, instance2)

    def test_unique_dict_02(self):
        """two instances if dict order is important, one if it's not"""
        with patch.object(TestUniquornCreation.UniquornTestClass2, "uniquorn_dict_order_matters", ["a"]):
            instance1 = TestUniquornCreation.UniquornTestClass2({"a": 1, "0": 0}, "b")
            instance2 = TestUniquornCreation.UniquornTestClass2({"0": 0, "a": 1}, "b")
            self.assertIsNot(instance1, instance2)
            #
            instance1 = TestUniquornCreation.UniquornTestClass2("a", {"0": 0, "b": 1})
            instance2 = TestUniquornCreation.UniquornTestClass2("a", {"b": 1, "0": 0})
            self.assertIs(instance1, instance2)

        with patch.object(TestUniquornCreation.UniquornTestClass2, "uniquorn_dict_order_matters", ["b"]):
            instance1 = TestUniquornCreation.UniquornTestClass2({"a": 1, "0": 0}, "b")
            instance2 = TestUniquornCreation.UniquornTestClass2({"0": 0, "a": 1}, "b")
            self.assertIs(instance1, instance2)
            #
            instance1 = TestUniquornCreation.UniquornTestClass2("a", {"0": 0, "b": 1})
            instance2 = TestUniquornCreation.UniquornTestClass2("a", {"b": 1, "0": 0})
            self.assertIsNot(instance1, instance2)


if __name__ == '__main__':
    unittest.main()
