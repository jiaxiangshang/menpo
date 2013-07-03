import abc


class Transform(object):
    """
    An abstract representation of any n-dimensional transform.
    Provides a unified interface to apply the transform (:meth:`apply`)
    """
    __metaclass__ = abc.ABCMeta

    def apply(self, x, **kwargs):
        """
        Applies this transform to x. If x is `Transformable`,
        x will be handed this transform object to transform itself. If not,
        x is assumed to be a numpy array. The transformation will be non
        destructive, returning the transformed version. Any **kwargs will be
        passed to the specific transform _apply methods (see these for
        documentation on what are available)
        :param x:
        :param kwargs:
        :return:
        """
        def transform(x_):
            """ Local closure which calls the _apply method with the kwargs
            attached.
            """
            return self._apply(x_, **kwargs)
        try:
            x._transform(transform)
        except AttributeError:
            return self._apply(x, **kwargs)

    @abc.abstractmethod
    def _apply(self, x, **kwargs):
        """
        Applies the transform to the array x, returning the result.
        :param x:
        :raise:
        """
        pass

    @abc.abstractmethod
    def jacobian(self, shape):
        """
        Calculates the Jacobian of the warp - this may be constant
        :param shape
        """
        pass

    @abc.abstractmethod
    def compose(self, a):
        """
        Composes two transforms together: W(x;p) <- W(x;p) o W(x;delta_p)
        :param a: transform of the same type as this object
        """
        pass

    @abc.abstractproperty
    def inverse(self):
        """
        Returns the inverse of the transform, if applicable
        :raise NonInvertable if transform has no inverse
        """
        pass

    @classmethod
    @abc.abstractmethod
    def from_parameters(cls, p):
        """
        Build a transform from the provided 1D parameter array
        :param p: 1D parameter array
        """
        pass

    @abc.abstractproperty
    def parameters(self):
        """
        Return the parameters of the transform as a 1D ndarray
        """
        pass


class Transformable(object):
    """
    Interface for transformable objects. When Transform.apply() is called on
     an object, if the object has the method _transform,
     the method is called, passing in the transforms apply() method.
     This allows for the object to define how it should transform itself.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _transform(self, transform):
        """
        Apply the transform given to the Transformable object.
        """
        pass