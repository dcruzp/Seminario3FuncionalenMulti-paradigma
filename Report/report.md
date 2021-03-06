# Seminario 12. Características funcionales en lenguajes Multi-paradigma 

[TOC]

### Funciones como ciudadanos de primera clase 

Cuando se habla del termino ciudadano de primera clase, se refiere a que es un valor que puede ser asignado a variables, pasado como parámetro o devuelto como resultado de una función. C# también tiene `delegates` que básicamente son tipos a los que se les puede asignar cualquier tipo de método que coincida con su declaración (parámetros, tipos de datos y valor de retorno) 

```c#
Func<int,int> square = (x) => {return x * x };
Func<A,C> Compose<A,B,C>(Func<A,B> f , Func<B,C> g)
{
    return x => g(f(x)); 
}
Func<string,int> f1 = (str) =>{
    return str == "first" ? 1 : 0; 
};
Func<int,bool> f2 = (x) => {
    return x == 1; 
};
var fComposed = Compose(f1,f2);
Console.WriteLine(fCompose("secund")); //false
```

En el ejemplo anterior la función `Compose` toma como parámetro dos funciones que toman un parámetro y regresan un valor. Regresa una función que toma un parámetro del tipo que recibe el primer parámetro y regresa un valor del tipo del valor de retorno del segundo parámetro. 

Usando delegates también se tiene un comportamiento con la misma funcionalidad que vimos anteriormente. 

```c#
public delegate void Del (string message);

public static void DelegateMethod (string message)
{
    System.Console.WriteLine(message);
}

Del handler = DelegateMethod; 

handler("Hello World");

// Hello World
```

#### Comparación con Haskell

En Haskell las funciones son cuidadanos de primera clase , es decir pueden ser asignadas a una varaible , pasarse como argumento a otra funcion y devolverse como resultado 

El siguiente ejemplo muestra como funciona esta caractersitica en un lenguaje funcional como Haskell. 

```haskell
mapfunction :: (a -> b) -> [a] -> [b]
mapfunction _ [] = []
mapfunction f (x:xs) = f x : mapfunction f xs
```

Entonces si definimos una funcion para llamar a la funcion anterior pasandole los parametors definidos entoces estariamos llamando a la funcion `mapfunction` con la funcion `cube` que definiremos a continuacion.

```
cube :: Num a => a -> a
cube x = x**2
```

La salida de nuestro programa seria la evaluacion de la funcion en la lista que se pasa como argumento. por lo tanto tendriamos el resultado siguiente: 

```
*Main> mapfunction cube [2,3,4]
[4,9,16]
```



### Capacidades de pattern matching en C# 

Pattern matching en C# proporciona una sintaxis mas concisa para probar expresiones y tomar medidas cuando una expresión coincide. La expresión `is` admite pattern matching para probar una expresión y declarar condicionalmente una nueva variable al resultado de esa  expresión. La expresión `switch` permite realizar acciones basadas en el primer patrón coincidente de una expresión. Estas dos expresiones brindan un rico vocabulario de patrones.

##### Null Checks 

Uno de los escenarios mas comunes de los pattern matching es verificar que los valores no son `null`.  Tu puedes chequear y convertir un tipo que acepta valores `null` en su tipo subyacente mientras prueba el valor nulo 

```c#
int? maybe = 12;

if (maybe is int number)
{
    Console.WriteLine($"The nullable int 'maybe' has the value {number}");
}
else
{
    Console.WriteLine("The nullable int 'maybe' doesn't hold a value");
}
```

El código de arriba es un *declaration pattern* para chequear el tipo de la variable y asigna este a una nueva variable. La variable `number`  es solo accesible en el bloque `if` , si se trata de acceder  a esta variable en el bloque `else` o después del `if` este va a generar un error en tiempo de compilación. Debido a que no esta usando el operador `==`, este patrón funciona cuando un tipo sobrecarga el operador `==`. Eso lo convierte en una forma ideal de verificar valores de referencia nulos, agregando el patrón `not`.

```c#
string? message = "This is not the null string";

if (message is not null)
{
    Console.WriteLine(message);
}
```

El `not` es un patrón lógico que retorna verdadero cuando el cuando el patrón negado no machea.



##### Type tests 

Otro uso común de *pattern matching* es chequear una variable para ver de que tipo es. El siguiente ejemplo chequea si una variable no es `null` e implementa la interfaz `IList<T>`. Si la implementa esta usa la propiedad `Count`  de `ICollection<T>` para encontrar el indice medio.  El  *pattern matching* no coincide con un valor nulo, independientemente del tipo en tiempo de compilación de la variable. El código siguiente protege contra `null`, ademas de protegerse contra un tipo que no implementa `IList` 



```c#
public static T MidPoint<T>(IEnumerable<T> sequence)
{
    if (sequence is IList<T> list)
    {
        return list[list.Count / 2];
    }
    else if (sequence is null)
    {
        throw new ArgumentNullException(nameof(sequence), "Sequence can't be null.");
    }
    else
    {
        int halfLength = sequence.Count() / 2 - 1;
        if (halfLength < 0) halfLength = 0;
        return sequence.Skip(halfLength).First();
    }
}
```

Lo mismo se puede aplicar en una expresión `switch`  para comprobar que con múltiples tipos diferentes. 



##### Compare discrete values 

También se puede chequear una variable para encontrar si machea con un valor especifico. El siguiente código muestra un ejemplo donde se chequea un valor a través de todos los posibles valores declarados en una enumeración. 

```c#
public State PerformOperation(Operation command) =>
   command switch
   {
       Operation.SystemTest => RunDiagnostics(),
       Operation.Start => StartSystem(),
       Operation.Stop => StopSystem(),
       Operation.Reset => ResetToReady(),
       _ => throw new ArgumentException("Invalid enum value for command", nameof(command)),
   };
```

El ejemplo anterior muestra un método de envió basado en el valor de una enumeración. El caso final `_` es un `discard pattern` que machea todos los valores. Este  maneja cualquier error en la condicion donde el valor no machea con ninguno de los valores del `enum`.  Si se omite esa parte del bloque `switch` el compilador avisara que no se  puede manajar una respuesta para todas la posibles entradas.  En tiempo de ejecucion la expresion `switch` lanza una excepcion si el objeto que se examina no coincide con ninguno de los casos del `switch`. Se podria usar constantes numericas en lugar de de un conjunto de valores `enum` . Se puede usar tecnicas similares para valores de constantes de string que representan el comando 

```c#
public State PerformOperation(string command) =>
   command switch
   {
       "SystemTest" => RunDiagnostics(),
       "Start" => StartSystem(),
       "Stop" => StopSystem(),
       "Reset" => ResetToReady(),
       _ => throw new ArgumentException("Invalid string value for command", nameof(command)),
   };
```

 El ejemplo anterior muestra el mismo algoritmo pero usando valores string en lugar de un `enum` . En todos esos ejemplos *discard pattern* asegura que se cubren todas las entradas posibles.  El compilador asegura que cada posible entrada es manejada. 



##### Relational patterns 

Tu puedes usar *relational patterns* para probar como se compara un valor con las constantes.  Por ejemplo el siguiente codigo retorna el estado del agua basada en la temperatura en Fahrenheit: 

```c#
string WaterState(int tempInFahrenheit) =>
    tempInFahrenheit switch
    {
        (> 32) and (< 212) => "liquid",
        < 32 => "solid",
        > 212 => "gas",
        32 => "solid/liquid transition",
        212 => "liquid / gas transition",
    };
```

 El código anterior también muestra el *logical pattern* `and` para chequear que ambas condicionales se complen . Las dos sentecias  finales del `switch` dan salida a las dos posibles entradas que quedaban por asignar. Sin esas dos asignaciones el compilador avisaria que tu logica no cubre todas las entradas posibles. 

El código anterior también muestra otra importante característica que provee el compilador para las expresiones de *pattern matching*: El compilador te avisa si no se tratan todos los casos para todas las posibles entradas. Otra forma de de escribir la misma expresion puede ser: 

```c#
string WaterState2(int tempInFahrenheit) =>
    tempInFahrenheit switch
    {
        < 32 => "solid",
        32 => "solid/liquid transition",
        < 212 => "liquid",
        212 => "liquid / gas transition",
        _ => "gas",
};
```

La importancia de que el compilador valida si a todas las posibles entradas son procesadas radica en posibles Excepciones del programa, refractorizacion y reordenamiento del código. 

##### Multiple inputs 

Se pueden escribir patrones que examinan múltiples  propiedades de un objeto. Considera el siguiente *Order* `record` 

```c#
public record Order (int Item, decimal Cost); 
```

El siguiente código examina el numero de artículos y el valor de pedido para calcular un precio con descuento: 

```c#
public decimal CalculateDiscount(Order order) =>
    order switch
    {
        (Items: > 10, Cost: > 1000.00m) => 0.10m,
        (Items: > 5, Cost: > 500.00m) => 0.05m,
        Order { Cost: > 250.00m } => 0.02m,
        null => throw new ArgumentNullException(nameof(order), "Can't calculate discount on null order"),
        var someObject => 0m,
    };
```

Los primeros dos casos examinan dos propiedades del Order. La tercera examina solo el costo, la siguiente chequean el `null` y el final machea cualquier otra valor. Si el tipo Order define un método apropiado `Decontruct` tu puedes omitir la propiedad llamada del patrón y usar la deconstruccion para examinar las propiedades: 

```c#
public decimal CalculateDiscount(Order order) =>
    order switch
    {
        ( > 10,  > 1000.00m) => 0.10m,
        ( > 5, > 50.00m) => 0.05m,
        Order { Cost: > 250.00m } => 0.02m,
        null => throw new ArgumentNullException(nameof(order), "Can't calculate discount on null order"),
        var someObject => 0m,
    };
```

El codigo anterior muestra la *positional pattern* donde las propiedades son decontruidas por la expersion 



### List comprehension en C# 

Una List Comprehension en C# es un tipo de notación en el que el programador puede describir las propiedades que los miembros de un conjunto debe reunir. Son usualmente usado para crear un conjunto basado en otro ya existente aplicando algún tipo de combinación. 

Con la aparición de C# 3.0 y de .Net Framework 3.5, apareció la notación *List Comprehension* basada en `Linkq` . El siguiente ejemplo muestra como formar un conjunto de números pares en el rango del 0 al 10.

```c#
IEnumerable<int> numbers = Enumerable.Range(0, 10);
var evens = from num in numbers where num % 2 == 0 select num;
```

Esto nos va a dar a retornar un objeto `evens` que es una lista que contiene a todos los números pares del 0 al 10  , `0 2 4 6 8 ` 

Las *querys expression* en C# 3 en adelante son azúcar sintáctica sobre la nomenclatura del código de C# normal. Aunque las expresiones de consultas generalmente terminan llamando a métodos de extencion (No tienen que hacerlo y al compilador no le importa, pero generalmente si). Hay varias cosas que se pueden hacer con las colecciones que no están disponibles en las expresiones de consulta de C#, pero son compatibles con las llamadas a métodos, por lo que vale la pena conocer ambos tipos de sintaxis.

```c#
List<Foo> fooList = new List<Foo>();
IEnumerable<string> extract = from foo in fooList where foo.Bar > 10 select foo.Name.ToUpper();
```

es preprocesado en: 

```c#
List<Foo> fooList = new List<Foo>();
IEnumerable<string> extract = fooList.Where(foo => foo.Bar > 10)
                                     .Select(foo => foo.Name.ToUpper());
```

Si se quieren hacer filtros basados en el indice del valor en la colección original se puede usar una sobrecarga apropiada de `Where` que no es posible en las *query expression*  

```c#
List<Foo> fooList = new List<Foo>();
IEnumerable<string> extract = fooList.Where((foo, index) => foo.Bar > 10 + index)
                                     .Select(foo => foo.Name.ToUpper());
```

Tambien existe `List<T>.ConvertAll` que se comporta igual que las *list Comprehension* realizando la misma operacion en cada elemento de una lista existente y luego devolviendo una nueva coleccion. Esta es una alternativa al uso de `Linq`, especialmente si se esta usando .NET 2.0 . En el ejemplo siguiente se muestra como usar esta con C# 3.0 pasando una función lambda especificando la función de mapeo que se necesita.  

```c#
var foo = new List<int> {1,2,3}; 
var bar = foo.ConvertAll (x => x * 2);  //list comprehension 
Console.WriteLine(string.Join(" ", bar)); // should print 2,4,6
```

Para C# 2.0, tu puedes usar un método anónimo con el `delegate`  `Convert`  para hacer algo parecido. 

```c#
List<int> foo = new List<int> (new int[]{1,2,3}); 
var bar = foo.ConvertAll(new Converter<int, int>(delegate (int x) { return x * 2; }));
Console.WriteLine(string.Join(" ", bar));
```

 Esto se puede aplicar no solo a listas , tambien se pueden usar `Arrays` usando `Array.ConvertAll` 

#### Comparación con haskell 

Haskell tiene List Comprehension para describir estas facilidades que brindan otros lenguajes también. Por ejemplo podemos hacer lo siguiente en Haskell 

```haskell
Prelude> [n | n <- [2..5] , n `mod` 2 == 0]
[2,4]
```

Aquí obtendríamos los números pares que están entre el 2 y el 5, la forma de hacerlo es bastante sencilla, lo que nos da la facilidad de una expresividad mayor con pocas lineas de código. Este comportamiento se obtiene en C# usando querys o algunas otras particularidades que existen en C# para esto. En haskell también podríamos hacer algo como lo siguiente: 

```haskell
primos :: Int -> [Int] 
primos n = [ x | x <- [2..n] , esPrimo x]
```

Si nos damos cuenta es la misma sintaxis que en el ejemplo de arriba solo que aquí queríamos resaltar que `esPrimo ` es una función previamente declarada , por lo tanto podemos complejizar la sentencia tanto como se quiera. 

### Inferencia de Tipos en C# 

La inferencia de tipos es un proceso por el cual el compilador determina el tipo de una variable local que ha sido declarada sin una declaración explicita de su tipo. El tipo es inferido a partir del valor inicial provisto a la variable. Para que el algoritmo de inferencia de tipos funciones es necesaria una entrada, que es el contenido de la variable. Si no inicializamos la variable a inferir tendremos un error de compilación. La inferencia de tipos en C# se puede implementar haciendo uso de la palabra reservada `var` . la sintaxis para declarar una variable haciendo uso de la inferencia de tipos seria así: 

```c#
var x = new ArrayList(); 
```

en este caso el compilador determino que la variable `x` es del tipo `ArrayList` , pese a que en ningún momento se ha declarado su tipo explícitamente. 

La inferencia de tipos por valor generaliza al tipo mas implícito y optimizado del .Net Framework. Como el framework optimiza la performance para tipos enteros de 32-bits (System.Int32 y System.UInt32) un valor de 0,10 o de 100 que perfectamente podrían inferirse como `System.Byte` se infiere como system.Int32. Incluso se recomienda usar los tipos enteros para controladores (aunque contemos del 0 al 10) y variables enteras de acceso frecuente, ya que la performance en tiempo de ejecución del tipo entero es preferible al storage en RAM que ahorramos si declaramos variables como `System.SByte`, `System.Byte` y `System.Int16`. De la misma manera, con valores de punto flotante si declaramos una variable con un valor de 3.14 sera inferida al tipo `System.Double` y no como System.Single(float) que perfectamente se la puede contener. La razón es que las operaciones con System.Double son optimizadas por hardware. Solo se infiere a un tipo no optimizado por el Framework(como System.Int64 o System.Decimal)  si el valor de la variable esta fuera del rango de los tipos optimizados. Si por ejemplo queremos que se infiera el valor 3.14 como float en vez de double, debemos proporcionar cierta evidencia que ayude al compilador a inferirlo como float. 

``` c#
var inferredType = (float)3.14  // casting explicito 
var inferredType = 3.14f        // notacion sufijo 
```

Entonces resumiendo la inferencia de tipos no se resuelve utilizando mecanismo de código dinámico, que afecten la performance en tiempo de ejecución. La inferencia de tipos se resuelve en tiempo de compilación, por lo tanto existe un costo en tiempo de compilación, ese tiempo es el tiempo que tarda el algoritmo de inferencia en sintetizar una expresión y resolver el tipo de una variable.  La inferencia de tipos tanto de valor como de referencia es para variable locales de métodos. No se aplica para variables de clases, propiedades, parámetros ni valores de retorno. La inferencia de tipos no es mas que azúcar sintáctica, una manera cómoda y ágil de declarar variables locales.

#### Comparación con Haskell

En Haskell la inferencia de tipo es por defecto , es decir no existe un keyword especial para este proposito. Por ejemplo podemos definir una fucnion sin especificar tipo , pero el compilador determianara que tipo de funcion es y el tipo del valor de retorno: 

```
producto list = product list 
```

`product` es una función en Haskell para encontrar el producto entre números , en este caso de arriba el compilador asume que la función `producto` recibe una lista de enteros y devuelve un entero , es decir `producto :: [Int] -> Int`

### Tuplas en C# 

Las tuplas se crea utilizando los tipos genéricos `Tuple<T1>`  - `Tuple<T1,T2,T3,T4,T5,T6,T7,T8>`. Cada uno de los tipos representa una tupla que contiene de 1 a 8 elementos. Los tipos pueden ser de diferente tipos.

```c#
//tuple with 4 element
var tuple = new Tuple<string, int, bool, MyClass>("foo", 123, true, new MyClass());
```

Las tuplas también se pueden crear usando métodos estáticos de `Tuple.Create` .En este caso los tipos de los elementos son inferidos por el compilador de C#. 

```c#
// tuple with 4 elements
var tuple = Tuple.Create("foo", 123, true, new MyClass()); 
```

Desde C# 7.0 las tuplas se pueden crear facilmente usando  `ValueTuple`. 

```c#
var tuple = ("foo", 123, true, new MyClass()); 
```

Para acceder a los elementos de una tupla se utiliza `item1`- `item8` proopiedades. Solos las propiedades con numeros de indices menor o igual al tamano de las tupla estaran disponibles (es decir, no se puede acceder a las propiedad `Item3` en `Tuple<T1,T2>`). 

```c#
var tuple = new Tuple<string, int, bool, MyClass>("foo", 123, true, new MyClass());
var item1 = tuple.Item1; // "foo"
var item2 = tuple.Item2; // 123
var item3 = tuple.Item3; // true
var item4 = tuple.Item4; // new My Class()
```

Las tuplas se pueden comparar en función de sus elementos. Como ejemplo, un enumerable cuyos elementos son del tipo `Tuple` puede ordenarse en función de los operadores de comparación definidos en un elemento especifico: 

```c#
List<Tuple<int, string>> list = new List<Tuple<int, string>>();
list.Add(new Tuple<int, string>(2, "foo"));
list.Add(new Tuple<int, string>(1, "bar"));
list.Add(new Tuple<int, string>(3, "qux"));

list.Sort((a, b) => a.Item2.CompareTo(b.Item2)); //sort based on the string element

foreach (var element in list) {
    Console.WriteLine(element);
}

// Output
// (1, bar) 
// (2, foo) 
// (3, qux)
```

Las tuplas se pueden usar para devolver múltiples valores de un método sin usar parámetros. En el siguiente ejemplo, *AddMultiply* se usa para devolver dos valores(suma, producto). 

```c#
void Write()
{
    var result = AddMultiply(25, 28);
    Console.WriteLine(result.Item1);
    Console.WriteLine(result.Item2);
}

Tuple<int, int> AddMultiply(int a, int b)
{
    return new Tuple<int, int>(a + b, a * b);
}
// output:
// 53 
// 700
```

 Uno de los casos mas comunes de los usos de casos de las tuplas es como tipo de retorno de método. Es decir en lugar de definir los parámetros del método, puede agrupar los resultados del método en un tipo de retorno de tupla, como muestra el siguiente ejemplo: 

```c#
var xs = new [] {4,7,9};
var limits = FindMinMax(xs); 
Console.WriteLine($"Limits of [{string.Join(" ", xs)}] are {limits.min} and {limits.max}");
// Output:
// Limits of [4 7 9] are 4 and 9

var ys = new[] { -9, 0, 67, 100 };
var (minimum, maximum) = FindMinMax(ys);
Console.WriteLine($"Limits of [{string.Join(" ", ys)}] are {minimum} and {maximum}");
// Output:
// Limits of [-9 0 67 100] are -9 and 100

(int min , int max ) FindMinMax(int[] input)
{
    // ... code here
}
```

En el ejemplo anterior se puede ver como se puede trabajar con la tupla retornada directamente o desonstruyentdo esta en variables separadas. 

Se puede especificar explicitamente el nombre de cada uno de los campos de la inicialización de la tupla o la definición de el tipo de tupla, como se muestra en el siguiente ejemplo: 

```c#
var t = (Sum: 4.5, Count: 3);
Console.WriteLine($"Sum of {t.Count} elements is {t.Sum}.");

(double Sum, int Count) d = (4.5, 3);
Console.WriteLine($"Sum of {d.Count} elements is {d.Sum}.");
```

Con C# 7.1 si no se especifica el nombre de los campo, estos se van a inferir del nombre de la variable correspondiente en la expresión de inicialización de la tupla. como se muestra en la tupla siguiente: 

```c#
var sum = 4.5;
var count = 3;
var t = (sum, count);
Console.WriteLine($"Sum of {t.count} elements is {t.sum}.");
```

Eso se conoce como iniciadores de proyección de tuplas. El nombre de una variables no se proyecta en un nombre de campo de tuplas en los siguientes casos: 

 - el nombre del candidato es un nombre del miembro de un tipo de tupla, por ejemplo `Item3`, `ToString` o `Rest` 
 - el nombre del candidato es un duplicado de otro nombre de campo de tupla, ya sea explicito o implicito

En esos casos, especifica explicitamente el nombre de un campo o acceder a un campo por su nombre predeterminado. 

El nombre por defecto de los campos de las tuplas son `Item1`, `Item2`, `Item3` y así sucesivamente. Siempre se puede usar el nombre por defecto de un campo. Incluso cuando el nombre de un campo se especifica explícitamente o se infiere, como lo muestra el siguiente ejemplo: 

```c#
var a = 1;
var t = (a, b: 2, 3);
Console.WriteLine($"The 1st element is {t.Item1} (same as {t.a}).");
Console.WriteLine($"The 2nd element is {t.Item2} (same as {t.b}).");
Console.WriteLine($"The 3rd element is {t.Item3}.");
// Output:
// The 1st element is 1 (same as 1).
// The 2nd element is 2 (same as 2).
// The 3rd element is 3.
```

La asignación de tuplas y las comparaciones de igualdad de tuplas no tienen en cuenta los nombre de campos. En tiempo de compilación, el compilador remplaza los nombres de los campos que no son por defecto con los correspondientes nombres por defecto. Como resultado, los nombres de los campos explícitamente especificados o inferidos no están disponibles en tiempo de ejecución. 

C# soporta la asignación entre tipos de tuplas que satisfacen las dos condiciones siguientes: 

 - ambos tipos de tuplas tienen el mismo numero de elementos
 - por cada posición en la tupla, el tipo de la tupla de la derecha es el mismo o se puede convertir implícitamente al tipo que le corresponde al elemento de lado izquierdo

Los valores de los elementos de la tupla son asignados siguiendo el orden de los elementos de la tupla. El nombre de los campos de las tuplas son ignorados y no asignados, como se muestra en el siguiente ejemplo: 

```c#
(int, double) t1 = (17, 3.14);
(double First, double Second) t2 = (0.0, 1.0);
t2 = t1;
Console.WriteLine($"{nameof(t2)}: {t2.First} and {t2.Second}");
// Output:
// t2: 17 and 3.14

(double A, double B) t3 = (2.0, 3.0);
t3 = t2;
Console.WriteLine($"{nameof(t3)}: {t3.A} and {t3.B}");
// Output:
// t3: 17 and 3.14
```

Se puede usar el operador de asignación `=` para *deconstruir* la instancia de una tupla en variables separadas. Se puede hacer de una de las siguientes maneras.

 - Declarando explicitamente el tipo de cada variable dentro de parentesis: 

   ```c#
   var t = ("post office", 3.6);
   (string destination, double distance) = t;
   Console.WriteLine($"Distance to {destination} is {distance} kilometers.");
   // Output:
   // Distance to post office is 3.6 kilometers.
   ```

 - Usar la palabra reservada `var` fuera de los parentesis para declarar implicitamente los tipos de variables y dejar que le compilador infiera sus tipos. 

   ```c#
   var t = ("post office", 3.6);
   var (destination, distance) = t;
   Console.WriteLine($"Distance to {destination} is {distance} kilometers.");
   // Output:
   // Distance to post office is 3.6 kilometers.
   ```

 - Usar variables existentes: 

   ```c#
   var destination = string.Empty;
   var distance = 0.0;
   
   var t = ("post office", 3.6);
   (destination, distance) = t;
   Console.WriteLine($"Distance to {destination} is {distance} kilometers.");
   // Output:
   // Distance to post office is 3.6 kilometers.
   ```

La igualdad entre tuplas con C# 7.3, los tipos de tuplas soportan los operadores de `==` y `!=` Esos operadores comparan los miembros del lado izquierdo del operador con los miembros correspondientes del lado derecho del operador siguiendo el orden de los elementos de la tupla. 

```c#
(int a, byte b) left = (5, 10);
(long a, int b) right = (5, 10);
Console.WriteLine(left == right);  // output: True
Console.WriteLine(left != right);  // output: False

var t1 = (A: 5, B: 10);
var t2 = (B: 5, A: 10);
Console.WriteLine(t1 == t2);  // output: True
Console.WriteLine(t1 != t2);  // output: False
```

En el ejemplo anterior se muestra, las operaciones `==` y `!=` no tienen en cuenta los nombres de los campos de las tupas. 

Dos tuplas son comparables cuando cuando cumplen las dos condiciones siguientes: 

 - Ambas tuplas tienen el numero de elementos. 
 - Por cada posiciones de la tupla, los elementos correspondientes de la parte izquierda y de la parte derecha de operador son comparables con los operadores `==` y `!=` 

Típicamente, se factoriza un método que tiene parámetros `out` dentro de un método que retorna una tupla. Sin embargo hay casos en que un parámetro `out`  puede ser de un tipo tupla. Los ejemplos siguientes muestran como trabajar con tuplas como parametros`out`.

```c#
var limitsLookup = new Dictionary<int, (int Min, int Max)>()
{
    [2] = (4, 10),
    [4] = (10, 20),
    [6] = (0, 23)
};

if (limitsLookup.TryGetValue(4, out (int Min, int Max) limits))
{
    Console.WriteLine($"Found limits: min is {limits.Min}, max is {limits.Max}");
}
// Output:
// Found limits: min is 10, max is 20
```

  #### Comparación con Haskell 

En Haskell es bastante parecido a C# , la sintaxis es basntante parecida , las tupla son representadas con parentesis y los elementos son separados por `,` .Ejemplo

```haskell
Prelude> let tuple = (1,2,3)
Prelude> tuple
(1,2,3)
Prelude> :t tuple
tuple :: (Num a, Num b, Num c) => (a, b, c)
```

Los elementos de las tuplas pueden ser de dstinto tipo , como sucede en C#, ejemplo : 

```haskell
Prelude> let tuple = ("perro" , 4 , True)
Prelude> tuple
("perro",4,True)
```

Las tuplas pueden ser usadas  como valores de retorno en la función, para poder encapsular mas de una elemento el el retorno de una función, como se practica en C# tambien. 

### Redefinicion de operadores en C# 

Un tipo definido por el programador puede sobrecargar un operador de C# predefinido. Un tipo puede proporcionar la implementacion personalizada de una operación cuando uno o los dos operandos son de ese tipo. 

Para sobrecargar un operador se usa la palabla clave `operator` . Una declaración de operador debe cumplir con la siguiente reglas: 

 - Incluir los modificadores`public` y  `static`  
 - Un operador unitario tiene un parámetro de entrada. Un operador binario tiene dos parametros de entrada. En cada caso, al menos un parámetro debe ser de tipo `T` o `T?` donde `T` es el tipo que contiene la declaración del operador.

En el ejemplo siguiente se muestra una estructura simplificada para representar un numero racional. La estructura sobrecarga alguno de los operadores aritmético: 

```c#
using System;

public readonly struct Fraction
{
    private readonly int num;
    private readonly int den;

    public Fraction(int numerator, int denominator)
    {
        if (denominator == 0)
        {
            throw new ArgumentException("Denominator cannot be zero.", nameof(denominator));
        }
        num = numerator;
        den = denominator;
    }

    public static Fraction operator +(Fraction a) => a;
    public static Fraction operator -(Fraction a) => new Fraction(-a.num, a.den);

    public static Fraction operator +(Fraction a, Fraction b)
        => new Fraction(a.num * b.den + b.num * a.den, a.den * b.den);

    public static Fraction operator -(Fraction a, Fraction b)
        => a + (-b);

    public static Fraction operator *(Fraction a, Fraction b)
        => new Fraction(a.num * b.num, a.den * b.den);

    public static Fraction operator /(Fraction a, Fraction b)
    {
        if (b.num == 0)
        {
            throw new DivideByZeroException();
        }
        return new Fraction(a.num * b.den, a.den * b.num);
    }

    public override string ToString() => $"{num} / {den}";
}

public static class OperatorOverloading
{
    public static void Main()
    {
        var a = new Fraction(5, 4);
        var b = new Fraction(1, 2);
        Console.WriteLine(-a);   // output: -5 / 4
        Console.WriteLine(a + b);  // output: 14 / 8
        Console.WriteLine(a - b);  // output: 6 / 8
        Console.WriteLine(a * b);  // output: 5 / 8
        Console.WriteLine(a / b);  // output: 10 / 4
    }
}
```



#### Posibilidades de sobrecarga en C# 

La tabla siguiente muestra las posibilidades de sobrecarga de los operadores en C# 

| Operadores                                                   | Posibilida de sobrecarga                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `+x`, `-x`, `!x`, `~x`, `++`, `--`, `true`, `false`          | Estos operadores unarios se pueden sobrecargar               |
| `x + y`, `x-y`, `x * y`, `x / y`, `x % y`, `x & y`, `x ^ y`, `x << y`, `x >> y`, `x == y`, `x != y`, `x < y`, `x > y`, `x <= y`, `x >= y`, `x|y` | No se pueden sobrecargar los operadores lógicos condicionales, si un tipo con los operadores `true` o `false` sobrecargados, también sobrecarga al operador `&` o `|` de determinada manera, el operador `&&` o `||`, respectivamente, se puede evaluar para los operadores de este tipo. |
| `a[i]` , `a?[i]`                                             | El acceso a un elemento no se considera un operador sobrecargable, pero puede definir un indexador. |
| `(T)x`                                                       | No se puede convertir el operador de conversión, pero puede definirse conversiones de tipos personalizadas que pueden realizarse mediante una expresión de conversión |
| `+=`, `-=`, `*=`, `/=`, `%=`, `&=` ,`^=`, `<<=`, `>>=` , `|=` | Los operadores de asignación compuestos no pueden sobrecargarse explícitamente. Pero cuando se sobrecarga un operador binario, el operador de asignación compuesto correspondiente , si lo hay, también se puede sobrecargar de modo implícito. Por ejemplo `+= `se evalúa con `+` , que se pueden sobrecargar. |
| `^x`, `x = y`, `x.y`, `x?.y`, `c ? t : f`, `x ?? y`, `x ??= y`, `x..y`, `x->y`, `=>`, `f(x)`, `as`, `await`, `checked`, `unchecked`, `default`, `delegate`, `is`, `nameof`, `new`,`sizeof`, `stackalloc`, `switch`, `typeof`,`with` | Estos operadores no se pueden sobrecargar                    |

### Comparación con Haskell 

La sobrecarga en Haskell esta diponible utilizando clase de tipo . Por ejemplo para sobrecargar `+` , como `+` pertenece a `Num` por lo que habria qu eproporcionar una clase de tipo `Num` para su tipo. 

Se podria definir un nuevo operador por ejemplo: 

```haskell
data Pair a b = Pair a b
	deriving Show 
infixl 6 |+| -- optional; set same precedence and associativity as + 
Pair a b |+| Pair c d = Pair (a+c) (b+d)
```

Y si lo ejecutamos tendriamos el comportamiento deseado: 

```haskell
> Pair 2 4 |+| Pair 1 2 
Pair 3 6
```



### Inmutabilidad en C# 

Los tipos inmutables son esos que sus datos no pueden ser alterados después de que se crea la instancia. En tipos inmutables se crea en una nuevo espacio de memoria y los valores modificados son guardados en una nueva memoria. 

En C# los `string` son inmutables, que significa que se crea una nueva memoria cada vez que se altera el objeto, en vez de trabajar en el espacio de memoria donde ya existe la memoria. Esto se traduce en que cada vez que tratamos de modificar un string, un nuevo objeto va a ser referenciado donde va a estar el nuevo string y el espacio de memoria donde estaba el objeto anteriormente va a ser desreferenciado. Entonce si modificamos un string constantemente el numero de desreferenciacio a viejos objetos se incrementara y este proceso va a tener que esperar por el recolector de basura para liberar los espacios de memoria que han sido desreferenciados y la aplicación va disminuir su rendimiento.    

```c#
string str = string.Empty
for (int i = 0; i < 1000 ; i++)
{
    str += "string "
}
```

En el código de arriba `str` va a ser actualizado 1000 veces dentro de un ciclo y cada vez que se ejecuta el ciclo se crean nuevas instancias , entonces las valores antiguos vas a ser tratados por el recolector de basura después de algún tiempo. 

No es una buena practica la solución anterior, es mejor usar tipos mutables. En C# existen `StringBuilder` que es un tipo mutable. Esto significa que  siempre se usa la misma dirección de memoria para alterar el objeto, es decir se trabaja sobre la misma instancia, esto no va a crear ninguna instancia futura por lo tanto no va a disminuir el rendimiento de nuestra aplicación. 

```c#
StringBuilder = strB = new StringBuilder(); 
for (int i =0; i < 10000; i++)
{
    strB.Append("Modified "); 
}
```

 En el código anterior, no tiene un impacto grande sobre la memoria porque este no crea instancia cada vez que se ejecuta el cuerpo del ciclo. 

Para crear clases inmutables en C# , tenemos que pensar si sus propiedades o variables no van a cambiar nunca sus valores después que sean asignados la primera vez. 

Haciendo la variable de solo lectura tal que no se pueda modificar la variable después que se asigne la primera vez. Ejemplo: 

```c#
class MyClass
{
    private readonly string myStr;
    
    public MyClass(string str)
    {
        myStr = str;
    }
    
    public string GetStr
    {
        get {return myStr;}
    }
}
```

En el código anterior se tiene un campo de solo lectura que es inicializado a través del constructor de la clase. De esta manera se pueden crear la clases inmutables en C#

En C# existe el `namespace` , `System.Collections.Inmmutable` que contiene  colecciones inmutables. Contiene inmutables versiones de `List`, `Dictionaries`, `Arrays` , `Hashes` `Stacks` y `Queues`  

Por ejemplo `ImmutableStack<T>` puede ser usando para pushear y extraer elementos de la pila de la misma manera en que se hace con la implementaciones mutables de `Stack<T>` sin embargo `ImmutableStack<T>` es una colección inmutable, sus elementos no pueden ser alterados. Entonces cuando se hace una llamada a `pop`  para extraer un elemento de la pila, una nueva pila es creada y la pila original permanece inalterada.

Vamos a ver el siguiente ejemplo, en este caso vamos a ver como se pueden pushear elementos dentro de una pila inmutable. 

```c#
var stack = ImmutableStack<int>.Empty;
for(int i = 0; i < 10; i++)
{
    stack = stack.Push(i);
}
```

El código siguiente muestra que los elementos de una pila inmutable no pueden ser alterado. 

```c#
var stack = ImmutableStack<int>.Empty;
for(int i = 0; i < 10; i++)
{
	stack = stack.Push(i);
}
Console.WriteLine("No of elements in original stack:" + stack.Count());
var newStack = stack.Pop();
Console.WriteLine("No of elements in new stack: " + newStack.Count());
Console.ReadKey();

// No of elements in original stack: 10
// No of elements in new stack: 9
```

Como se puede ver en el resultado anterior  la pila inmutable original (contiene 10 elementos) no ha cambiado después de la llamada al método `pop()`. En cambio una nueva pila inmutables es creada con 9 elementos  

Las colecciones inmutables no tiene constructor pero se puede usar el método estático `Create` como se muestra en el código a continuación:

```c#
var list = ImmutableList.Create(1,2,3,4,5);
```

Si se quiere añadir o eliminar un elemento de esta colección, una nueva lista inmutable sera creada  y la lista original permanecerá igual.s

