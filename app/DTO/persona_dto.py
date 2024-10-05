
from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, id, nombre, apellido, telefono, mail, usuario, psw):
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido 
        self.__telefono = telefono
        self.__mail = mail
        self.__usuario = usuario
        self.__psw = psw

    def get_id(self):
        return self.__id
    def set_id(self,id):
        self.__id = id

    def get_nombre(self):
        return self.__nombre
    def set_nombre(self,nombre):
        self.__nombre = nombre

    def get_apellido(self):
        return self.__apellido
    def set_apellido(self,apellido):
        self.__apellido = apellido

    def get_telefono(self):
        return self.__telefono
    def set_telefono(self,telefono):
        self.__telefono = telefono

    def get_mail(self):
        return self.__mail
    def set_mail(self,mail):
        self.__mail = mail

    def get_usuario(self):
        return self.__usuario
    def set_usuario(self, usuario):
        self.__usuario = usuario

    def get_psw(self):
        return self.__psw
    def set_psw(self,psw):
        self.__psw = psw


    def __str__(self):
        txt = f"ID = {self.__id}\n"
        txt += f"Nombre = {self.__nombre} {self.__apellido}\n"
        txt += f"Telefono = {self.__telefono}\n"
        txt += f"Mail = {self.__mail}\n"
        txt += f"Usuario = {self.__usuario}\n"
        txt += f"Contraseña = {self.__psw}\n"
        return txt



