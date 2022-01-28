from numpy import character
import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w,x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        if nn.as_scalar(self.run(x)) >= 0:
            return 1
        else:
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        while True:
            flag = True
            #iterate the dataset
            for x,node in dataset.iterate_once(1):
                if self.get_prediction(x) == nn.as_scalar(node):
                    continue
                else:
                    #update weight
                    self.w.update(x,nn.as_scalar(node))
                    flag = False
                    
            if flag:
                break
        

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        #a three layer net, f(x) = relu(relu(x*W1+b1)*W2+b2)*W3+b3
        self.rand_size = 50 #random determined by myself, couldn't find a precise one
        self.w1 = nn.Parameter(1, self.rand_size)
        self.b1 = nn.Parameter(1, self.rand_size)
        self.w2 = nn.Parameter(self.rand_size, self.rand_size)
        self.b2 = nn.Parameter(1, self.rand_size)
        self.w3 = nn.Parameter(self.rand_size, 1)
        self.b3 = nn.Parameter(1, 1)
        
        self.param_list = [self.w1,self.w2,self.w3,self.b1,self.b2,self.b3]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.param_list[0]), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.param_list[1]), self.b2))
        
        xm = nn.Linear(layer2, self.w3)
        return nn.AddBias(xm, self.b3)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(1):
                gradient = nn.gradients(self.get_loss(x, y), self.param_list)
                #-0.05 is random find. Using this number is because it does pretty fast.
                for i in range(len(self.param_list)):
                    self.param_list[i].update(gradient[i],-0.05)
            #Your implementation will receive full points if it gets a loss of 0.02 or better
            #For the best performance just 0.02 is OK.
            if nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))) < 0.02:
                return

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        #a three layer net, f(x) = relu(relu(x*W1+b1)*W2+b2)*W3+b3
        #notice that Each output we provide is a 10-dimensional vector which has zeros, so b3 should be 1*10, w3
        #should be 100*10
        self.rand_size = 100 #random determined by myself, couldn't find a precise one
        self.w1 = nn.Parameter(28*28, self.rand_size)
        self.b1 = nn.Parameter(1, self.rand_size)
        self.w2 = nn.Parameter(self.rand_size, self.rand_size)
        self.b2 = nn.Parameter(1, self.rand_size)
        self.w3 = nn.Parameter(self.rand_size, 10)
        self.b3 = nn.Parameter(1, 10)
        
        self.param_list = [self.w1,self.w2,self.w3,self.b1,self.b2,self.b3]
        
    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.param_list[0]), self.b1))
        layer2 = nn.ReLU(nn.AddBias(nn.Linear(layer1, self.param_list[1]), self.b2))
        
        xm = nn.Linear(layer2, self.w3)
        return nn.AddBias(xm, self.b3)
    
    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)
     
    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(6):
                gradient = nn.gradients(self.get_loss(x, y), self.param_list)
 
                for i in range(len(self.param_list)):
                    self.param_list[i].update(gradient[i],-0.05)
            #Your implementation will receive full points if it gets a accuracy lager than 0.97
            if dataset.get_validation_accuracy() >= 0.97:
                return

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.rand_size = 100
        self.w1 = nn.Parameter(self.num_chars, self.rand_size)
        self.b1 = nn.Parameter(1, self.rand_size)
        self.w2 = nn.Parameter(self.num_chars, self.rand_size)
        self.Whidden = nn.Parameter(self.rand_size,self.rand_size)
        self.b2 = nn.Parameter(1, self.rand_size)
        self.w3 = nn.Parameter(self.rand_size, 5)
        self.b3 = nn.Parameter(1, 5)
        
        self.param_list = [self.w1,self.w2,self.Whidden,self.w3,self.b3,self.b2,self.b1]

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        #z_0 = x_0*W, using AddBias to calculate h_1
        h_i = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.param_list[0]),self.param_list[-1]))
        #normal iteration
        for i in range(1,len(xs)):
            character_i = xs[i]
            #z_i = x_i*W + h_i*W_hidden,using AddBias to calculate h_i+1
            z_i = nn.Add(nn.Linear(character_i, self.param_list[1]),nn.Linear(h_i, self.param_list[2]))
            h_i = nn.ReLU(nn.AddBias(z_i, self.param_list[-2]))
        h_final = nn.AddBias(nn.Linear(h_i,self.param_list[3]),self.param_list[-3])
        return h_final

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(3):
                gradient = nn.gradients(self.get_loss(x, y), self.param_list)
 
                for i in range(len(self.param_list)):
                    self.param_list[i].update(gradient[i],-0.005)
            #Your implementation will receive full points if it gets a accuracy at least 0.81
            if dataset.get_validation_accuracy() > 0.81:
                return