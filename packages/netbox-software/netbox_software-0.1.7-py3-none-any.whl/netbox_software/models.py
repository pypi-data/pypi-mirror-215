from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class Vendor(NetBoxModel):
    name = models.CharField(verbose_name="название", max_length=100, help_text='Укажите производителя ПО')
    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Разработчики"
        verbose_name = "Разработчик"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:vendor', args=[self.pk])

    def get_devices_count(self):
        return DeviceSoftware.objects.filter(vendor=self).count()

    def get_devices(self):
        devices = []
        dev_softs = DeviceSoftware.objects.filter(vendor=self)
        for soft in dev_softs:
            devices.append(soft.device.name)
        return DeviceSoftware.objects.filter(vendor=self)

    def get_software_count(self):
        return DeviceSoftware.objects.filter(vendor=self).count() + VirtualMachineSoftware.objects.filter(vendor=self).count()

    def get_software(self):
        soft_list = []
        dev_softs = DeviceSoftware.objects.filter(vendor=self)
        for soft in dev_softs:
            soft_list.append(soft)
        vm_softs = VirtualMachineSoftware.objects.filter(vendor=self)
        for soft in vm_softs:
            soft_list.append(soft)
        return soft_list


class SoftwareType(NetBoxModel):
    name = models.CharField(verbose_name="название", max_length=100, help_text='Укажите тип ПО')
    comments = models.TextField(verbose_name="комментарий", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Типы ПО"
        verbose_name = "Тип ПО"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:softwaretype', args=[self.pk])

    def get_devices_count(self):
        return DeviceSoftware.objects.filter(software_type=self).count()

    def get_devices(self):
        return DeviceSoftware.objects.filter(software_type=self)


class DeviceSoftware(NetBoxModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        help_text='Укажите имя, которое будет отображаться для этого ПО.'
    )

    device = models.ForeignKey(
        verbose_name="устройство",
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='software'
    )

    software_type = models.ForeignKey(
        to=SoftwareType,
        verbose_name="тип ПО",
        on_delete=models.CASCADE,
        related_name='device_software'
    )

    vendor = models.ForeignKey(
        to=Vendor,
        verbose_name="Разработчик",
        on_delete=models.CASCADE,
        related_name='device_software'
    )

    version = models.CharField(
        verbose_name="версия",
        max_length=50,
        blank=True
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "ПО устройств"
        verbose_name = "ПО устройства"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:devicesoftware', args=[self.pk])

    def get_devices(self):
        return DeviceSoftware.objects.filter(vendor=self.vendor).count() + \
            VirtualMachineSoftware.objects.filter(vendor=self.vendor).count()

    def get_software(self):
        return list(DeviceSoftware.objects.filter(vendor=self.vendor)) + list(
            VirtualMachineSoftware.objects.filter(vendor=self.vendor))


class VirtualMachineSoftware(NetBoxModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        help_text='Укажите имя, которое будет отображаться для этого ПО.'
    )

    virtual_machine = models.ForeignKey(
        verbose_name="виртуальая машина",
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='software'
    )

    software_type = models.ForeignKey(
        to=SoftwareType,
        verbose_name="тип ПО",
        on_delete=models.CASCADE,
        related_name='vm_software'
    )

    vendor = models.ForeignKey(
        to=Vendor,
        verbose_name="Разработчик",
        on_delete=models.CASCADE,
        related_name='vm_software'
    )

    version = models.CharField(
        verbose_name="версия",
        max_length=50,
        blank=True
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "ПО виртуальных машин"
        verbose_name = "ПО виртуальной машины"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_software:virtualmachinesoftware', args=[self.pk])

    def get_software_count(self):
        return DeviceSoftware.objects.filter(name=self.name).count() + \
            VirtualMachineSoftware.objects.filter(name=self.name).count()

    def get_software(self):
        return list(DeviceSoftware.objects.filter(vendor=self.vendor)) + list(
            VirtualMachineSoftware.objects.filter(vendor=self.vendor))
