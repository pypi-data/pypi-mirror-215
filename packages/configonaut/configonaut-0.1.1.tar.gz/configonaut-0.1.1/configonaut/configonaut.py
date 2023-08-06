import json


class Configonaut:
    """
    A Config class to handle operations related to a configuration stored in JSON format.

    Attributes
    ----------
    filename : str
        Name of the JSON file that stores the configuration.
    root : dict
        Root dictionary that contains the full configuration.
    current_dict : dict
        Current level of configuration.
    path : list
        List of dictionaries representing the path to the current level of configuration.
    """

    def __init__(self, filename='config.json', root=None, path=None):
        """
        Create a new Config instance.

        Parameters
        ----------
        filename : str, optional
            Name of the JSON file that stores the configuration.
        root : dict, optional
            Root dictionary that contains the full configuration.
        path : list, optional
            List of dictionaries representing the path to the current level of configuration.
        """
        self.filename = filename
        if root is None:
            self.root = self._load_config()
            path = [self.root]
        else:
            self.root = root
        self.current_dict = path[-1]
        self.path = path

    def _load_config(self):
        """
        Load configuration from JSON file.

        Returns
        -------
        dict
            The loaded configuration.
        """
        try:
            with open(self.filename, 'r') as configfile:
                return json.load(configfile)
        except FileNotFoundError:
            return {}

    def __getitem__(self, key):
        """
        Get an item from the configuration. If the item does not exist, a new item is created.

        Parameters
        ----------
        key : str or int or slice
            Key or index of the item.

        Returns
        -------
        Config or value
            If the item is a dictionary, return a new Config instance; otherwise, return the item's value.
        """
        if isinstance(key, slice):
            key, default = key.start, key.stop
            return self.get(key, default, save=True)
        if isinstance(key, int):
            key = list(self.current_dict.keys())[key]
        if key not in self.current_dict:
            self.current_dict[key] = {}
        return self._handle_dict_item(key)

    def _handle_dict_item(self, key):
        """
        Handle a dictionary item in the configuration.

        Parameters
        ----------
        key : str
            Key of the item.

        Returns
        -------
        Config or value
            If the item is a dictionary, return a new Config instance; otherwise, return the item's value.
        """
        if isinstance(self.current_dict[key], dict):
            new_path = self.path.copy()
            new_path.append(self.current_dict[key])
            return Configonaut(self.filename, self.root, new_path)
        else:
            return self.current_dict[key]

    def get_or_raise(self, key):
        """
        Get an item from the configuration. If the item does not exist, raise a KeyError.

        Parameters
        ----------
        key : str
            Key of the item.

        Returns
        -------
        Config or value
            If the item is a dictionary, return a new Config instance; otherwise, return the item's value.

        Raises
        ------
        KeyError
            If the item does not exist in the configuration.
        """
        if key not in self.current_dict:
            raise KeyError(key)
        return self._handle_dict_item(key)

    def to_value(self):
        """
        Get the current level of configuration as a dictionary.

        Returns
        -------
        dict
            The current level of configuration.
        """
        return self.current_dict

    def get(self, key, default=None, save=False):
        """
        Get an item from the configuration. If the item does not exist, return a default value and
        optionally save the default value to the configuration.

        Parameters
        ----------
        key : str
            Key of the item.
        default : any, optional
            Default value to return if the item does not exist.
        save : bool, optional
            Whether to save the default value to the configuration.

        Returns
        -------
        Config or value
            If the item is a dictionary, return a new Config instance; otherwise, return the item's value.
        """
        try:
            return self._handle_dict_item(key)
        except KeyError:
            if save:
                self.current_dict[key] = default
            return default

    def get_root(self):
        """
        Get the root of the configuration.

        Returns
        -------
        Configonaut
            A new Config instance that points to the root of the configuration.
        """
        return Configonaut(self.filename, self.root, [self.root])

    def previous(self):
        """
        Get the previous level of configuration.

        Returns
        -------
        Configonaut
            A new Config instance that points to the previous level of configuration.
        """
        if len(self.path) > 1:
            return Configonaut(self.filename, self.root, self.path[:-1])
        else:
            return self

    def __setitem__(self, key, value):
        """
        Set a new item in the configuration and save the configuration.

        Parameters
        ----------
        key : str
            Key of the item.
        value : any
            Value of the item.
        """
        self.current_dict[key] = value
        self.save()

    def __str__(self):
        """
        Return a string representation of the current level of configuration.

        Returns
        -------
        str
            A string representation of the current level of configuration.
        """
        return str(self.current_dict)

    def __repr__(self):
        """
        Return a string representation of the current level of configuration.

        Returns
        -------
        str
            A string representation of the current level of configuration.
        """
        return str(self.current_dict)

    def __iter__(self):
        """
        Get an iterator over the keys of the current level of configuration.

        Returns
        -------
        iterator
            An iterator over the keys of the current level of configuration.
        """
        return iter(self.current_dict)

    def items(self):
        """
        Get an iterator over the items of the current level of configuration. Each item is a tuple
        containing a key and a value. If the value is a dictionary, it is wrapped in a new Config instance.

        Returns
        -------
        iterator
            An iterator over the items of the current level of configuration.
        """
        for key, value in self.current_dict.items():
            if isinstance(value, dict):
                path = self.path.copy()
                path.append(value)
                yield key, Configonaut(self.filename, self.root, path)
            else:
                yield key, value

    def __len__(self):
        """
        Get the number of items in the current level of configuration.

        Returns
        -------
        int
            The number of items in the current level of configuration.
        """
        return len(self.current_dict)

    def __contains__(self, key):
        """
        Check if an item exists in the current level of configuration.

        Parameters
        ----------
        key : str
            Key of the item.

        Returns
        -------
        bool
            True if the item exists, False otherwise.
        """
        return key in self.current_dict

    def __delitem__(self, key):
        """
        Delete an item from the current level of configuration and save the configuration.

        Parameters
        ----------
        key : str
            Key of the item.
        """
        del self.current_dict[key]
        self.save()

    def save(self):
        """
        Save the configuration to the JSON file.
        """
        with open(self.filename, 'w') as configfile:
            json.dump(self.root, configfile, indent=4)
