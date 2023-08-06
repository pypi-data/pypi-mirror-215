from typing import overload
import typing

import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.Storage
import QuantConnect.Packets
import System
import System.Collections
import System.Collections.Generic

QuantConnect_Lean_Engine_Storage__EventContainer_Callable = typing.TypeVar("QuantConnect_Lean_Engine_Storage__EventContainer_Callable")
QuantConnect_Lean_Engine_Storage__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Lean_Engine_Storage__EventContainer_ReturnType")


class LocalObjectStore(System.Object, QuantConnect.Interfaces.IObjectStore, typing.Iterable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]):
    """A local disk implementation of IObjectStore."""

    NoReadPermissionsError: str = ...
    """
    No read permissions error message
    
    This field is protected.
    """

    NoWritePermissionsError: str = ...
    """
    No write permissions error message
    
    This field is protected.
    """

    @property
    def ErrorRaised(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Interfaces.ObjectStoreErrorRaisedEventArgs], None], None]:
        """Event raised each time there's an error"""
        ...

    @ErrorRaised.setter
    def ErrorRaised(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Interfaces.ObjectStoreErrorRaisedEventArgs], None], None]):
        """Event raised each time there's an error"""
        ...

    DefaultObjectStore: str
    """Gets the default object store location"""

    @property
    def Controls(self) -> QuantConnect.Packets.Controls:
        """
        Provides access to the controls governing behavior of this instance, such as the persistence interval
        
        This property is protected.
        """
        ...

    @Controls.setter
    def Controls(self, value: QuantConnect.Packets.Controls):
        """
        Provides access to the controls governing behavior of this instance, such as the persistence interval
        
        This property is protected.
        """
        ...

    @property
    def AlgorithmStorageRoot(self) -> str:
        """
        The root storage folder for the algorithm
        
        This property is protected.
        """
        ...

    @AlgorithmStorageRoot.setter
    def AlgorithmStorageRoot(self, value: str):
        """
        The root storage folder for the algorithm
        
        This property is protected.
        """
        ...

    def ContainsKey(self, key: str) -> bool:
        """
        Determines whether the store contains data for the specified key
        
        :param key: The object key
        :returns: True if the key was found.
        """
        ...

    def Delete(self, key: str) -> bool:
        """
        Deletes the object data for the specified key
        
        :param key: The object key
        :returns: True if the delete operation was successful.
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    @overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an enumerator that iterates through a collection.
        
        :returns: An System.Collections.IEnumerator object that can be used to iterate through the collection.
        """
        ...

    def GetFilePath(self, key: str) -> str:
        """
        Returns the file path for the specified key
        
        :param key: The object key
        :returns: The path for the file.
        """
        ...

    def Initialize(self, algorithmName: str, userId: int, projectId: int, userToken: str, controls: QuantConnect.Packets.Controls) -> None:
        """
        Initializes the object store
        
        :param algorithmName: The algorithm name
        :param userId: The user id
        :param projectId: The project id
        :param userToken: The user token
        :param controls: The job controls instance
        """
        ...

    def InternalSaveBytes(self, key: str, contents: typing.List[int]) -> bool:
        """
        Won't trigger persist nor will check storage write permissions, useful on initialization since it allows read only permissions to load the object store
        
        This method is protected.
        """
        ...

    def LoadExistingObjects(self) -> None:
        """
        Loads objects from the AlgorithmStorageRoot into the ObjectStore
        
        This method is protected.
        """
        ...

    def OnErrorRaised(self, error: System.Exception) -> None:
        """
        Event invocator for the ErrorRaised event
        
        This method is protected.
        """
        ...

    def PathForKey(self, key: str) -> str:
        """
        Get's a file path for a given key.
        Internal use only because it does not guarantee the existence of the file.
        
        This method is protected.
        """
        ...

    def PersistData(self, data: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]) -> bool:
        """
        Overridable persistence function
        
        This method is protected.
        
        :param data: The data to be persisted
        :returns: True if persistence was successful, otherwise false.
        """
        ...

    def ReadBytes(self, key: str) -> typing.List[int]:
        """
        Returns the object data for the specified key
        
        :param key: The object key
        :returns: A byte array containing the data.
        """
        ...

    def SaveBytes(self, key: str, contents: typing.List[int]) -> bool:
        """
        Saves the object data for the specified key
        
        :param key: The object key
        :param contents: The object data
        :returns: True if the save operation was successful.
        """
        ...


class StorageLimitExceededException(System.Exception):
    """Exception thrown when the object store storage limit has been exceeded"""

    def __init__(self, message: str) -> None:
        """
        Creates a new instance of the storage limit exceeded exception
        
        :param message: The associated message
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Lean_Engine_Storage__EventContainer_Callable, QuantConnect_Lean_Engine_Storage__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Lean_Engine_Storage__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Lean_Engine_Storage__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Lean_Engine_Storage__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


